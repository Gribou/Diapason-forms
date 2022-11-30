from django.contrib.auth.models import Group
from constance import config as const_config
from django.conf import settings

from custom.serializers import get_available_forms
from sso.keycloak import has_keycloak_config
from .forms import TeamSerializer, GroupSerializer
from ..models import config


def get_serialized_config():
    result = {
        'features': {
            'show_stats': const_config.SHOW_STATS,
            'atco_mode': const_config.ATCO_MODE,
            'stripless': const_config.ATCO_MODE != "CAUTRA",
            'has_zones': config.TeamZone.objects.exists(),
            'notifications': get_serialized_notifications(),
            'gallery_url': const_config.GALLERY_URL,
            'sso': has_keycloak_config()
        },
        'teams': TeamSerializer(config.Team.objects.select_related("zone").all(), many=True).data,
        'groups': GroupSerializer(Group.objects.prefetch_related('permissions').all(), many=True).data,
        'sectors': [s.label for s in config.Sector.objects.all()],
        'positions': [p.label for p in config.Position.objects.all()],
        'sector_groups': [g.label for g in config.SectorGroup.objects.all()],
        'custom_forms': get_available_forms(),
        'version': settings.VERSION_TAG
    }
    return result


def get_serialized_notifications():
    return [
        {"name": "fne",
            "label": "Notifications d'évènements (FNE)", "permission": "shared.be_notified_on_fne"},
        {"name": "similitude", "label": "Similitude d'Indicatifs",
            "permission": "shared.be_notified_on_simi"},
        {"name": "brouillage", "label": "Brouillage",
            "permission": "shared.be_notified_on_brouillage"}
    ]


def is_graph_complete(action_model):
    return not action_model.objects.filter(is_complete=False).exists()


def is_graph_checked(action_model):
    return not action_model.objects.filter(is_complete__isnull=True).exists()
