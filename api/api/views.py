from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.status import HTTP_204_NO_CONTENT

from constance import config

from shared.serializers import get_serialized_config, get_serialized_counters
from efne.serializers import get_serialized_fne_config, get_fne_list_metadata
from efne.models import FneCounter, Fne
from similitude.serializers import get_simi_list_metadata, get_serialized_simi_config
from similitude.models import SimiCounter, Simi
from brouillage.serializers import get_serialized_brouillage_config, get_brouillage_list_metadata
from brouillage.models import BrouillageCounter, Brouillage


class ConfigViewSet(ViewSet):
    """
    Fournit les éléments de configuration du site et des formulaires.
    Ces éléments sont uniquement modifiables par l'administrateur
    Ex : fonctionnalités actives ou non, remplissage des listes de sélection, ... 
    """

    def list(self, request):
        return Response({
            "shared": get_serialized_config(),
            "fne": get_serialized_fne_config(),
            "similitude": get_serialized_simi_config(),
            "brouillage": get_serialized_brouillage_config()
        })


class FormsMetaViewSet(ViewSet):
    """
        Fournit des éléments résumant les formulaires accessibles par l'utilisateur en cours.
        Est utilisé pour améliorer les performances de la page liste (on laisse le serveur calculer les filtres, le nombre de formulaires, etc. sans avoir à récupérer l'ensemble des formulaires côté frontend)
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        fne = get_fne_list_metadata(request.user)
        similitude = get_simi_list_metadata(request.user)
        brouillage = get_brouillage_list_metadata(request.user)
        return Response({
            "empty": not (fne['count'] and fne['relevant']) and
            not (similitude['count'] and similitude['relevant']) and
            not (brouillage['count'] and brouillage['relevant']),
            "assigned_count": self.get_assigned_forms_count(request),
            "forms": {
                "fne": fne,
                "similitude": similitude,
                "brouillage": brouillage,
            }
        })

    def get_assigned_forms_count(self, request):
        # counts how many forms are currently waiting and assigned to this user (aka to one of his/her groups)
        # this is not the same queryset as the one used in get_<>_list_metadata
        return sum(
            [model.objects.filter(
                status__is_waiting=True,
                assigned_to_group__in=request.user.groups.all()
            ).count() for model in [Fne, Simi, Brouillage]])


class AnyFormActivated(BasePermission):
    def has_permission(self, request, view):
        return (config.SHOW_FNE or config.SHOW_SIMI or config.SHOW_BROUILLAGE) and super().has_permission(request, view)


class CounterViewSet(ViewSet):
    """
    Statistiques d'utilisation de eFNE.
    'category_graph' et 'form_graph' sont formatés pour être utilisé avec ChartJS
    """
    permission_classes = [AnyFormActivated]

    def list(self, request):
        models = []
        if config.SHOW_FNE:
            models.append(FneCounter)
        if config.SHOW_SIMI:
            models.append(SimiCounter)
        if config.SHOW_BROUILLAGE:
            models.append(BrouillageCounter)
        return Response(get_serialized_counters(models))


class HealthCheckView(APIView):
    '''
    Vérification que le serveur web est en route
    A utiliser avec Docker-compose pour établir l'état de santé du container
    (healthcheck)
    '''

    def get(self, request, format=None):
        return Response(status=HTTP_204_NO_CONTENT)
