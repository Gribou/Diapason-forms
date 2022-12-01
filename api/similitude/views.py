from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny

from shared.mixins import (
    FormViewMixin, DraftViewMixin, InvestigatorViewMixin, RootViewMixin)
from shared.permissions import GroupRestricted, IsOwner
from shared.export import encode_image
from .models import Aircraft, Simi, SubData, PostIt
from .serializers import SimiSerializer, SimiWithSubDataSerializer, SimiPostItSerializer
from .permissions import SimiActivated
from .safetycube import SimiFormatter


class SimiModelMixin(FormViewMixin):
    serializer_class = SimiSerializer

    def update(self, request, *args, **kwargs):
        # see 'clean_incoming_media' in shared/mixins/FormViewMixin for explanation
        for a in request.data.get('aircrafts', []):
            if not a.get('strip', None) and a.get('pk', None):
                existing_aircraft = Aircraft.objects.filter(pk=a['pk'])
                if existing_aircraft.exists():
                    self.clean_incoming_media(
                        a, existing_aircraft.first().strip, 'strip', 'strip_url')
        return super().update(request, *args, **kwargs)

    def get_model(self):
        return Simi


class DraftSimiViewSet(SimiModelMixin, DraftViewMixin, viewsets.GenericViewSet):
    ''' Brouillons de Fiches similitude
    /api/similitude/draft/{uuid}/ pour accéder à un brouillon
    Les utilisateurs non authentifiés peuvent créer et mettre à jour les brouillons. Ils peuvent accéder à un brouillon donné grâce à son UUID mais ils ne peuvent pas lister l'ensemble des brouillons (pour maintenir autant que possible l'anonymat).'''
    queryset = Simi.objects.filter(status__is_draft=True)
    permission_classes = [SimiActivated, AllowAny]


class SimiViewSet(SimiModelMixin, InvestigatorViewMixin,  viewsets.ModelViewSet):
    '''
    Fiches similitude en cours de traitement.
    /api/similitude/form/{uuid}/ pour accéder à un formulaire donné
    Les utilisateurs authentifiés ont accès aux formulaires qui leur sont attribués.
    '''
    queryset = Simi.objects.all()
    permission_classes = [SimiActivated, GroupRestricted]
    serializer_class = SimiWithSubDataSerializer
    search_fields = InvestigatorViewMixin.search_fields + [
        'description', 'aircrafts__callsign', 'sub_data__inca_number']
    safetycube_formatter_class = SimiFormatter

    def get_export_context(self, request):
        context = super().get_export_context(request)
        instance = self.get_object()
        context.update({
            'form':
            instance,
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
            return SubData.objects.create(parent_simi=instance)

    def get_postit_model(self):
        return PostIt


class PostItViewSet(RootViewMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
    Post-its associés à une fiche similitude (pour mise à jour uniquement).
    /api/similitude/postit/{pk}/ pour accéder à un postit donné.
    '''
    queryset = PostIt.objects.all()
    serializer_class = SimiPostItSerializer
    permission_classes = [SimiActivated, IsOwner]
