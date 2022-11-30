
from djoser.serializers import UserSerializer
from rest_framework import serializers

from shared.serializers.config import GroupSerializer
from efne.models import FneAction
from similitude.models import SimiAction
from brouillage.models import BrouillageAction


class CustomUserSerializer(UserSerializer):
    is_sso = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    form_relevance = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + (
            'groups', 'is_sso', 'form_relevance', 'permissions')

    def to_representation(self, instance):
        ''' show nested object on read, expect pk on write'''
        response = super().to_representation(instance)
        response['groups'] = GroupSerializer(instance.groups, many=True).data
        return response

    def get_permissions(self, obj):
        return obj.get_all_permissions()

    def get_is_sso(self, obj):
        try:
            return obj.sso_profile.sub is not None
        except:
            return False

    def get_form_relevance(self, obj):
        # can the user get attributed a form of this type according to action graphs
        return {
            'fne': self.is_form_relevant(obj, FneAction),
            'similitude': self.is_form_relevant(obj, SimiAction),
            'brouillage': self.is_form_relevant(obj, BrouillageAction)
        }

    def is_form_relevant(self, obj, action_model):
        for g in obj.groups.all():
            if action_model.objects.filter(current_group=g).exists():
                return True
        return False
