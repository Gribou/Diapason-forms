from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny

from shared.mixins import (
    FormViewMixin, DraftViewMixin, InvestigatorViewMixin, RootViewMixin)
from shared.permissions import GroupRestricted, IsOwner
from shared.export import encode_image

from .models import Aircraft, Brouillage, SubData, PostIt
from .serializers import BrouillageSerializer, BrouillageWithSubDataSerializer, BrouillagePostItSerializer
from .permissions import BrouillageActivated


class BrouillageModelMixin(FormViewMixin):
    serializer_class = BrouillageSerializer

    def get_model(self):
        return Brouillage

    def update(self, request, *args, **kwargs):
        # see 'clean_incoming_media' for explanation
        for a in request.data.get('aircrafts', []):
            if not a.get('strip', None) and a.get('pk', None):
                existing_aircraft = Aircraft.objects.filter(pk=a['pk'])
                if existing_aircraft.exists():
                    self.clean_incoming_media(
                        a, existing_aircraft.first().strip, 'strip', 'strip_url')
        return super().update(request, *args, **kwargs)


class DraftBrouillageViewSet(BrouillageModelMixin, DraftViewMixin, viewsets.GenericViewSet):
    ''' Brouillons de fiche brouillage
    /api/brouillage/draft/{uuid}/ pour accéder à un brouillon
    Les utilisateurs non authentifiés peuvent créer et mettre à jour les brouillons. Ils peuvent accéder à un brouillon donné grâce à son UUID mais ils ne peuvent pas lister l'ensemble des brouillons (pour maintenir autant que possible l'anonymat).'''
    queryset = Brouillage.objects.filter(status__is_draft=True)
    permission_classes = [BrouillageActivated, AllowAny]


class BrouillageViewSet(BrouillageModelMixin, InvestigatorViewMixin, viewsets.ModelViewSet):
    '''
    Fiches brouillage en cours de traitement.
    /api/brouillage/form/{uuid}/ pour accéder à un formulaire donné
    Les utilisateurs authentifiés ont accès aux formulaires qui leur sont attribués.
    '''
    queryset = Brouillage.objects.all()
    permission_classes = [BrouillageActivated, GroupRestricted]
    serializer_class = BrouillageWithSubDataSerializer
    ordering = ['-event_date']
    search_fields = InvestigatorViewMixin.search_fields + [
        'description', 'aircrafts__callsign', 'aircrafts__waypoint', 'sub_data__inca_number']

    def get_export_context(self, request):
        context = super().get_export_context(request)
        instance = self.get_object()
        context.update({
            'form': instance,
            'encoded_strips': [
                encode_image(a.strip)
                for a in instance.aircrafts.all()
            ],
        })
        return context

    def get_postit_parent(self, instance):
        try:
            return instance.sub_data
        except ObjectDoesNotExist:
            return SubData.objects.create(parent=instance)

    def get_postit_model(self):
        return PostIt


class PostItViewSet(RootViewMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
    Post-its associés à une fiche brouillage (pour mise à jour uniquement).
    /api/brouillage/postit/{pk}/ pour accéder à un postit donné.
    '''
    queryset = PostIt.objects.all()
    serializer_class = BrouillagePostItSerializer
    permission_classes = [BrouillageActivated, IsOwner]
