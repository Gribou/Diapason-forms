from rest_framework import serializers
from django.db import transaction
from constance import config

from shared.serializers import (
    PostItSerializer, ActionSerializer, FormSerializer, RedactorSerializer, is_form_relevant_to_user, get_assigned_forms, get_metadata_from_forms, is_graph_complete, is_graph_checked)
from shared.safetycube.utils import is_safetycube_enabled
from . import models


class SimiRedactorSerializer(RedactorSerializer):
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
        fields = ['pk', 'callsign', 'strip', 'strip_url', 'position',
                  'type', 'provenance', 'destination', 'ssr', 'fl']


class SimiPostItSerializer(PostItSerializer):
    class Meta(PostItSerializer.Meta):
        model = models.PostIt


class SubDataSerializer(serializers.ModelSerializer):
    postits = SimiPostItSerializer(many=True, read_only=True)

    class Meta:
        model = models.SubData
        fields = ['postits', 'inca_number']


class SimiActionSerializer(ActionSerializer):

    class Meta(ActionSerializer.Meta):
        model = models.SimiAction


class SimiSerializer(FormSerializer):
    redactors = SimiRedactorSerializer(many=True, required=False)
    aircrafts = AircraftSerializer(many=True, required=False)
    available_actions = SimiActionSerializer(many=True, read_only=True)

    class Meta(FormSerializer.Meta):
        model = models.Simi
        fields = FormSerializer.Meta.fields + [
            'redactors', 'aircrafts', 'description', 'with_incident']

    def create(self, validated_data):
        with transaction.atomic():
            redactors = validated_data.pop('redactors', [])
            aircrafts = validated_data.pop('aircrafts', [])
            simi = super().create(validated_data)
            for r in redactors:
                models.Redactor.objects.create(simi=simi, **r)
            for a in aircrafts:
                models.Aircraft.objects.create(simi=simi, **a)
            # do not edit sub data here. It should be edited in
            # SimiWithSubDataSerializer
            simi.save()  # force counters update taking redactors into account
            return simi

    def update(self, instance, validated_data):
        with transaction.atomic():
            redactors = validated_data.pop('redactors', [])
            aircrafts = validated_data.pop('aircrafts', [])
            # update redactor children (delete and replace)
            instance.redactors.all().delete()
            for r in redactors:
                models.Redactor.objects.create(simi=instance, **r)
            # update aircraft children (delete and replace)
            instance.aircrafts.all().delete()
            for a in aircrafts:
                models.Aircraft.objects.create(simi=instance, **a)
            # do not edit sub data here. It should be edited in
            # SimiWithSubDataSerializer
            return super().update(instance, validated_data)


class SimiWithSubDataSerializer(SimiSerializer):
    sub_data = SubDataSerializer(required=False)

    class Meta(SimiSerializer.Meta):
        model = models.Simi
        fields = SimiSerializer.Meta.fields + \
            ['sub_data']

    def create(self, validated_data):
        with transaction.atomic():
            sub_data = validated_data.pop("sub_data", None)
            simi = super().create(validated_data)
            if sub_data:  # may be empty
                models.SubData.objects.create(parent_simi=simi, **sub_data)
            return simi

    def update(self, instance, validated_data):
        with transaction.atomic():
            sub_data = validated_data.pop("sub_data", None)
            # postits are not updated in batch. They are only edited one by one
            if sub_data:
                sub_data.pop("postits", None)
            instance = super().update(instance, validated_data)
            # update sub data (do not delete and replace so that postits can
            # persist)
            if sub_data:
                models.SubData.objects.update_or_create(parent_simi=instance,
                                                        defaults=sub_data)
            else:
                models.SubData.objects.filter(parent_simi=instance).delete()
            instance.refresh_from_db()
            return instance


def get_simi_list_metadata(user):
    forms = get_assigned_forms(user, models.Simi)
    return {
        "relevant": is_form_relevant_to_user(user, models.SimiAction),
        **get_metadata_from_forms(forms)
    }


def get_serialized_simi_config():
    return {
        'enabled': config.SHOW_SIMI,
        'save_button_label': config.SIMI_SAVE_BUTTON_LABEL,
        'cds_warning_enabled': config.SIMI_CDS_WARNING_ENABLED,
        'safetycube_enabled': models.Simi.options.is_safetycube_enabled(),
        "graph": {
            'complete': is_graph_complete(models.SimiAction),
            'checked': is_graph_checked(models.SimiAction)
        }
    }
