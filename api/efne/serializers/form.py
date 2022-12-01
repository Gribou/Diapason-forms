from rest_framework import serializers
from django.db import transaction
from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist
import mimetypes

from shared.serializers import (RedactorSerializer,
                                ActionSerializer, FormSerializer,  is_form_relevant_to_user, get_assigned_forms, get_metadata_from_forms)
from shared.fields import Base64ImageField
from shared.export import encode_image
from shared.models.config import user_has_all_access
from shared.validators import validate_uploaded_file_size
from .. import models
from .config import EventTypeSerializer, TechEventTypeSerializer, TechActionSerializer


class FneRedactorSerializer(RedactorSerializer):
    class Meta(RedactorSerializer.Meta):
        model = models.Redactor
        fields = ['fullname', 'role', 'team', 'email']


class AircraftSerializer(serializers.ModelSerializer):
    strip = serializers.FileField(
        write_only=True,
        allow_empty_file=True,
        required=False,
    )
    strip_url = serializers.FileField(source='strip', read_only=True)

    class Meta:
        model = models.Aircraft
        fields = ['pk', 'callsign', 'strip', 'strip_url']


class TCASReportAircraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TCASReportAircraft
        fields = [
            'callsign', 'ssr', 'flight_phase', 'real_fl', 'assigned_fl',
            'is_origin', 'is_vfr', 'is_mil', 'advisory_type', 'contact_radio'
        ]


class TCASReportSerializer(serializers.ModelSerializer):
    aircrafts = TCASReportAircraftSerializer(many=True)

    class Meta:
        model = models.TCASReport
        fields = [
            'pilote_min_distance', 'pilote_min_altitude', 'ctl_min_distance',
            'ctl_min_altitude', 'aircrafts', 'traffic_info', 'pilot_request',
            'before_manoeuvre', 'pilot_action_required', 'disrupted_traffic',
            'asr', 'safety_net'
        ]


class CdsReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CdsReport
        fields = ['com_cds', 'rex_cds', "notif_rpo", 'cpi']


class AttachmentSerializer(serializers.ModelSerializer):
    file_url = serializers.FileField(source="file", read_only=True)
    file = serializers.FileField(write_only=True)
    size = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    by_me = serializers.SerializerMethodField()
    author = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Attachment
        fields = ['pk', 'file', 'file_url', 'size', 'author', 'by_me', 'type']

    def get_size(self, obj):
        try:
            return self._pretty_size(obj.file.size)
        except:
            return self._pretty_size(0)

    def get_type(self, obj):
        return next(iter(mimetypes.guess_type(obj.file.url)), None)

    def _pretty_size(self, value):
        if value < 512000:
            value = value / 1024.0
            ext = 'ko'
        elif value < 4194304000:
            value = value / 1048576.0
            ext = 'Mo'
        else:
            value = value / 1073741824.0
            ext = 'Go'
        return '%s %s' % (str(round(value, 2)), ext)

    def get_by_me(self, obj):
        try:
            user = self.context['request'].user
            return user_has_all_access(user) or (obj.author.pk == user.pk if obj.author is not None else not user.is_authenticated)
        except:
            # if serializer is triggered by a background task, request may be null
            return False

    def validate_file(self, file):
        validate_uploaded_file_size(file)
        return file


class FneActionSerializer(ActionSerializer):

    class Meta(ActionSerializer.Meta):
        model = models.FneAction


class FneSerializer(FormSerializer):
    redactors = FneRedactorSerializer(many=True, required=False)
    aircrafts = AircraftSerializer(many=True, required=False)
    tcas_report = TCASReportSerializer(required=False)
    cds_report = CdsReportSerializer(required=False)
    available_actions = FneActionSerializer(many=True, read_only=True)
    drawing = Base64ImageField(
        required=False, allow_empty_file=True, allow_null=True)
    drawing_url = serializers.FileField(source='drawing', read_only=True)
    attachments = AttachmentSerializer(many=True, required=False)
    zones = serializers.SerializerMethodField()

    class Meta(FormSerializer.Meta):
        model = models.Fne
        fields = FormSerializer.Meta.fields + [
            'secteur', 'position', 'regroupement', 'lieu', 'isp', 'event_types',
            'description', 'cds_report', 'redactors', 'aircrafts',
            'tcas_report', 'drawing', 'drawing_url',
            'tech_event', 'tech_actions_done', 'attachments', 'zones'
        ]

    def get_zones(self, obj):
        return obj.redactors.values(name=F("team__zone__short_name"), color=F("team__zone__color")).order_by("name").distinct()

    def to_representation(self, instance):
        ''' show nested object on read, expect pk on write'''
        response = super().to_representation(instance)
        response['event_types'] = EventTypeSerializer(
            instance.event_types.all(), many=True).data
        response['tech_event'] = TechEventTypeSerializer(
            instance.tech_event.all(), many=True).data
        response['tech_actions_done'] = TechActionSerializer(
            instance.tech_actions_done.all(), many=True).data
        response['drawing'] = encode_image(instance.drawing).get(
            "data", None) if instance.drawing is not None else None
        return response

    def validate(self, data):
        # if type is TCAS, tcas_report must be present
        tcas_event = models.EventType.objects.get(is_tcas=True)
        if (tcas_event is not None and tcas_event in data.get(
                'event_types', [])) and (data.get('tcas_report', None) is None):
            raise serializers.ValidationError(
                "Un CR TCAS doit être fourni si l'évènement est de catégorie 'TCAS'"
            )
        return data

    def validate_attachments(self, attachments):
        for a in attachments:
            if "file" in a:
                validate_uploaded_file_size(a.get('file'))
        return attachments

    def create(self, validated_data):
        # handles nested object creation
        with transaction.atomic():
            redactors = validated_data.pop('redactors', [])
            aircrafts = validated_data.pop('aircrafts', [])
            tcas_report = validated_data.pop('tcas_report', None)
            cds_report = validated_data.pop('cds_report', None)
            attachments = validated_data.pop('attachments', [])
            fne = super().create(validated_data)
            if tcas_report:  # report may be empty
                self._create_tcas_report(fne, tcas_report)
            if cds_report:  # may be empty
                models.CdsReport.objects.create(parent_fne=fne, **cds_report)
            for r in redactors:
                models.Redactor.objects.create(fne=fne, **r)
            for a in aircrafts:
                models.Aircraft.objects.create(fne=fne, **a)
            user = self.context['request'].user
            author = user if user.is_authenticated else None
            for a in attachments:
                models.Attachment.objects.create(
                    parent=fne, author=author, **a)
            # do not edit sub data here. It should be edited in
            # FneWithSubDataSerializer
            fne.save()  # force counters update taking redactors into account
            return fne

    def _create_tcas_report(self, instance, validated_report):
        aircrafts = validated_report.pop("aircrafts", [])
        tcas_report = models.TCASReport.objects.create(parent_fne=instance,
                                                       **validated_report)
        for a in aircrafts:
            models.TCASReportAircraft.objects.create(parent_report=tcas_report,
                                                     **a)

    def update(self, instance, validated_data):
        # handles nested object update
        with transaction.atomic():
            redactors = validated_data.pop('redactors', [])
            aircrafts = validated_data.pop('aircrafts', [])
            tcas_report = validated_data.pop('tcas_report', None)
            event_types = validated_data.pop('event_types', [])
            tech_event = validated_data.pop("tech_event", [])
            tech_actions_done = validated_data.pop("tech_actions_done", [])
            cds_report = validated_data.pop('cds_report', None)
            # attachments are handled in dedicated endpoints and do not need to be handled here
            # see AttachmentViewSet and  add_attachment extra action on FneViewSet
            validated_data.pop('attachments', [])

            instance.event_types.set(event_types)
            instance.tech_event.set(tech_event)
            instance.tech_actions_done.set(tech_actions_done)
            # update redactor children (delete and replace)
            instance.redactors.all().delete()
            for r in redactors:
                models.Redactor.objects.create(fne=instance, **r)
            # update aircraft children (delete and replace)
            instance.aircrafts.all().delete()
            for a in aircrafts:
                models.Aircraft.objects.create(fne=instance, **a)
            # update tcas report (delete and replace if present)
            try:
                instance.tcas_report.delete()
            except ObjectDoesNotExist:
                pass
            if tcas_report:
                self._create_tcas_report(instance, tcas_report)
            # update cds report (delete and replace if present)
            try:
                instance.cds_report.delete()
            except ObjectDoesNotExist:
                pass
            if cds_report:
                models.CdsReport.objects.create(parent_fne=instance,
                                                **cds_report)
            # do not edit sub data here. It should be edited in
            # FneWithSubDataSerializer
            return super().update(instance, validated_data)


def get_fne_list_metadata(user):
    forms = get_assigned_forms(user, models.Fne)
    sub_forms = forms.exclude(sub_data__isnull=True) \
        .exclude(sub_data__alarm_acknowledged=True)
    warnings = len([f for f in sub_forms
                    if f.sub_data.has_warning and not f.sub_data.has_alarm])
    alarms = len([f for f in sub_forms if f.sub_data.has_alarm])
    event_types = forms.prefetch_related("event_types") \
        .exclude(event_types__isnull=True) \
        .values_list("event_types__name", flat=True)
    return {
        "relevant": is_form_relevant_to_user(user, models.FneAction),
        "warnings": warnings,
        "alarms": alarms,
        "event_types": sorted(event_types.order_by().distinct()),
        **get_metadata_from_forms(forms)
    }
