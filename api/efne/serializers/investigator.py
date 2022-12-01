from rest_framework import serializers
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from .. import models
from shared.serializers import PostItSerializer
from .form import FneSerializer, AttachmentSerializer


class FnePostItSerializer(PostItSerializer):
    class Meta(PostItSerializer.Meta):
        model = models.PostIt


class SubDataSerializer(serializers.ModelSerializer):
    postits = FnePostItSerializer(many=True, read_only=True)

    class Meta:
        model = models.SubData
        fields = ['postits', 'inca_number', 'hn',
                  'is_safety_event', 'alarm_acknowledged']


class FneWithSubDataSerializer(FneSerializer):
    sub_data = SubDataSerializer(required=False)
    has_warning = serializers.SerializerMethodField()
    has_alarm = serializers.SerializerMethodField()

    class Meta(FneSerializer.Meta):
        model = models.Fne
        fields = FneSerializer.Meta.fields + \
            ['sub_data', 'has_warning', 'has_alarm']

    def get_has_warning(self, obj):
        try:
            return obj.sub_data.has_warning
        except ObjectDoesNotExist:
            return False

    def get_has_alarm(self, obj):
        try:
            return obj.sub_data.has_alarm
        except ObjectDoesNotExist:
            return False

    def get_answer(self, obj):
        # TODO get attchments from safetycube
        answer = super().get_answer(obj)
        if answer:
            answer['attachments'] = AttachmentSerializer(
                obj.attachments.all(), many=True).data
            answer['attachments'] = [a if a.get('author', None) else {
                'include': True, **a} for a in answer['attachments']]
        return answer

    def create(self, validated_data):
        # handles nested object creation
        with transaction.atomic():
            sub_data = validated_data.pop("sub_data", None)
            fne = super().create(validated_data)
            if sub_data:  # may be empty
                models.SubData.objects.create(parent_fne=fne, **sub_data)
            return fne

    def update(self, instance, validated_data):
        # handles nested object update
        with transaction.atomic():
            sub_data = validated_data.pop("sub_data", None)
            # postits are not updated in batch. They are only edited one by one
            if sub_data:
                sub_data.pop("postits", None)
            instance = super().update(instance, validated_data)
            # update sub data (do not delete and replace so that postits can
            # persist)
            if sub_data:
                # provide defaults value for hn, because if hn is not present, it is not updated and set to None as it should be
                # and null values are not sent by frontend
                defaults = {
                    'hn': sub_data.pop('hn', None),
                    **sub_data,
                }
                models.SubData.objects.update_or_create(parent_fne=instance,
                                                        defaults=defaults)
            else:
                models.SubData.objects.filter(parent_fne=instance).delete()
            instance.refresh_from_db()
            return instance
