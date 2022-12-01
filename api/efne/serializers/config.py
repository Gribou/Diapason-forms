from rest_framework import serializers
from constance import config

from .. import models
from shared.serializers import is_graph_complete, is_graph_checked
from shared.safetycube.utils import is_safetycube_enabled


class EventTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.EventType
        fields = ['pk', 'name', 'rank', 'is_tcas']


class TechActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TechAction
        fields = ['pk', 'name', 'helperText']


class TechEventTypeSerializer(serializers.ModelSerializer):
    actions = TechActionSerializer(many=True)

    class Meta:
        model = models.TechEventType
        fields = ['pk', 'name', 'helperText', 'rank', 'actions']


def get_serialized_fne_config():
    return {
        'enabled': config.SHOW_FNE,
        'event_types':
        EventTypeSerializer(models.EventType.objects.all(), many=True).data,
        'tech_event_types':
        TechEventTypeSerializer(models.TechEventType.objects.prefetch_related("actions").all(),
                                many=True).data,
        'roles': [r.label for r in models.Role.objects.all()],
        'save_button_label': config.FNE_SAVE_BUTTON_LABEL,
        'cds_warning_enabled': config.FNE_CDS_WARNING_ENABLED,
        'safetycube_enabled': models.Fne.options.is_safetycube_enabled(),
        'graph': {
            'complete': is_graph_complete(models.FneAction),
            'checked': is_graph_checked(models.FneAction)
        }
    }
