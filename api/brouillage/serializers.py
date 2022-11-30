from rest_framework import serializers
from django.db import transaction
from django.db.models import F
from constance import config

from shared.serializers import ActionSerializer, FormSerializer, PostItSerializer, RedactorSerializer, get_assigned_forms, is_form_relevant_to_user, get_metadata_from_forms, is_graph_complete, is_graph_checked
from . import models


class InterferenceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.InterferenceType
        fields = ['pk', 'name', 'rank']


def get_serialized_brouillage_config():
    return {
        'enabled': config.SHOW_BROUILLAGE,
        'interference_types':
        InterferenceTypeSerializer(models.InterferenceType.objects.all(),
                                   many=True).data,
        'save_button_label': config.BROUILLAGE_SAVE_BUTTON_LABEL,
        'cds_warning_enabled': config.BROUILLAGE_CDS_WARNING_ENABLED,
        "graph": {
            'complete': is_graph_complete(models.BrouillageAction),
            'checked': is_graph_checked(models.BrouillageAction)
        }
    }


class BrouillageRedactorSerializer(RedactorSerializer):

    class Meta(RedactorSerializer.Meta):
        model = models.Redactor


class AircraftSerializer(serializers.ModelSerializer):
    strip = serializers.FileField(
        write_only=True,
        allow_empty_file=True,
        required=False,
    )
    strip_url = serializers.FileField(source='strip', read_only=True)

    class Meta:
        model = models.Aircraft
        fields = ['pk', 'callsign', 'strip',
                  'strip_url', 'fl', 'waypoint', 'distance', 'bearing', 'plaintiff']


class BrouillagePostItSerializer(PostItSerializer):
    class Meta(PostItSerializer.Meta):
        model = models.PostIt


class SubDataSerializer(serializers.ModelSerializer):
    postits = BrouillagePostItSerializer(many=True, read_only=True)

    class Meta:
        model = models.SubData
        fields = ['postits']


class BrouillageActionSerializer(ActionSerializer):
    class Meta(ActionSerializer.Meta):
        model = models.BrouillageAction


class BrouillageSerializer(FormSerializer):
    redactors = BrouillageRedactorSerializer(many=True, required=False)
    aircrafts = AircraftSerializer(many=True, required=False)
    available_actions = BrouillageActionSerializer(many=True, read_only=True)
    zones = serializers.SerializerMethodField()

    class Meta(FormSerializer.Meta):
        model = models.Brouillage
        fields = FormSerializer.Meta.fields + \
            ['redactors', 'aircrafts', 'interferences',
                'frequency', 'description', 'cwp', 'zones',
                'freq_unusable', 'traffic_impact', 'supp_freq']

    def to_representation(self, instance):
        ''' show nested object on read, expect pk on write'''
        response = super().to_representation(instance)
        response['interferences'] = InterferenceTypeSerializer(
            instance.interferences.all(), many=True).data
        return response

    def get_zones(self, obj):
        return obj.redactors.values(name=F("team__zone__short_name"), color=F("team__zone__color")).order_by("name").distinct()

    def create(self, validated_data):
        with transaction.atomic():
            redactors = validated_data.pop('redactors', [])
            aircrafts = validated_data.pop('aircrafts', [])
            brouillage = super().create(validated_data)
            for r in redactors:
                models.Redactor.objects.create(brouillage=brouillage, **r)
            for a in aircrafts:
                models.Aircraft.objects.create(brouillage=brouillage, **a)
            # do not edit sub data here. It should be edited in
            # BrouillageWithSubDataSerializer
            brouillage.save()  # force counters update taking redactors into account
            return brouillage

    def update(self, instance, validated_data):
        with transaction.atomic():
            redactors = validated_data.pop('redactors', [])
            aircrafts = validated_data.pop('aircrafts', [])
            interferences = validated_data.pop('interferences', [])
            instance.interferences.set(interferences)
            # update redactor children (delete and replace)
            instance.redactors.all().delete()
            for r in redactors:
                models.Redactor.objects.create(brouillage=instance, **r)
            # update aircraft children (delete and replace)
            instance.aircrafts.all().delete()
            for a in aircrafts:
                models.Aircraft.objects.create(brouillage=instance, **a)
            # do not edit sub data here. It should be edited in
            # BrouillageWithSubDataSerializer
            return super().update(instance, validated_data)


class BrouillageWithSubDataSerializer(BrouillageSerializer):
    sub_data = SubDataSerializer(required=False)

    class Meta(BrouillageSerializer.Meta):
        fields = BrouillageSerializer.Meta.fields + ['sub_data']


def get_brouillage_list_metadata(user):
    forms = get_assigned_forms(user, models.Brouillage)
    return {
        "relevant": is_form_relevant_to_user(user, models.BrouillageAction),
        **get_metadata_from_forms(forms)
    }
