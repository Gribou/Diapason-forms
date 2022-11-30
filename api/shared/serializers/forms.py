from django.contrib.auth.models import Group
from rest_framework import serializers

from ..models import config, form, investigator
from ..answer import serialize_answer_suggestion


class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.SlugRelatedField(
        slug_field="codename", many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['pk', 'name', 'permissions', ]


class TeamSerializer(serializers.ModelSerializer):
    zone = serializers.StringRelatedField()

    class Meta:
        model = config.Team
        fields = ['pk', 'label', 'zone']


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = form.Status
        fields = [
            'pk', 'label', 'is_draft', 'is_waiting', 'is_in_progress',
            'is_done', 'is_to_be_deleted'
        ]


class SafetyCubeSerializer(serializers.ModelSerializer):
    class Meta:
        model = investigator.SafetyCubeRef
        fields = ['reference', 'url', 'status']


class FormSerializer(serializers.ModelSerializer):
    status = StatusSerializer(read_only=True)
    assigned_to_group = GroupSerializer(read_only=True)
    next_form = serializers.SerializerMethodField()
    previous_form = serializers.SerializerMethodField()
    safetycube = SafetyCubeSerializer(read_only=True)
    answer = serializers.SerializerMethodField()

    # this serializer needs to be inherited with a non-abstract Meta.model

    class Meta:
        model = form.AbstractForm
        fields = [
            'status', 'assigned_to_group', 'assigned_to_person',
            'creation_date', 'update_date', 'event_date', "uuid", 'available_actions', 'next_form', 'previous_form', 'keywords',
            'safetycube', 'answer'
        ]
        extra_kwargs = {'event_date': {'required': True}}
        read_only_fields = ['assigned_to_person',
                            'creation_date', 'update_date', 'uuid', 'available_actions', 'next_form', 'previous_form',
                            'safetycube', 'answer']

    def get_next_form(self, obj):
        try:
            items = self.context['items']
            current_rank = items.index(obj.uuid)
            return items[current_rank+1]
        except (IndexError, ValueError, KeyError):
            return None

    def get_previous_form(self, obj):
        try:
            items = self.context['items']
            current_rank = items.index(obj.uuid)
            if current_rank > 0:
                return items[current_rank-1]
        except (IndexError, ValueError, KeyError):
            return None

    def get_answer(self, obj):
        return serialize_answer_suggestion(obj) if config.user_is_investigator(self.context['request'].user) else None


class ActionSerializer(serializers.ModelSerializer):
    next_status = StatusSerializer()

    # this serializer needs to be inherited with a non-abstract Meta.model

    class Meta:
        model = form.AbstractAction
        fields = ['label', 'next_status', 'next_group']


class PostItSerializer(serializers.ModelSerializer):
    by_me = serializers.SerializerMethodField()
    author = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())
    parent_form = serializers.SerializerMethodField()

    class Meta:
        model = investigator.AbstractPostIt
        fields = [
            'pk', 'content', 'author', 'creation_date', 'update_date', 'by_me', 'parent_form'
        ]

    def get_by_me(self, obj):
        return obj.author.pk == self.context['request'].user.pk

    def get_parent_form(self, obj):
        return obj.get_parent().uuid


class RedactorSerializer(serializers.ModelSerializer):
    team = serializers.SlugRelatedField(
        slug_field="label", allow_null=True, queryset=config.Team.objects.all())

    class Meta:
        fields = ['fullname', 'team', 'email']

    def to_representation(self, instance):
        ''' show nested object on read, expect label on write'''
        response = super().to_representation(instance)
        response['team'] = TeamSerializer(instance.team).data
        return response
