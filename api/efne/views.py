from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.core.exceptions import ObjectDoesNotExist
from PIL import Image

from shared.mixins import (
    FormViewMixin, DraftViewMixin, InvestigatorViewMixin, RootViewMixin)
from shared.export import encode_image
from shared.permissions import GroupRestricted, IsOwner
from shared.validators import validate_uploaded_file_size

from .models import Fne, Aircraft, PostIt, SubData, Attachment
from .serializers import FneSerializer, FneWithSubDataSerializer, AttachmentSerializer, FnePostItSerializer
from .permissions import FneActivated
from .safetycube import FneFormatter


class FneModelMixin(FormViewMixin):
    serializer_class = FneSerializer

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
        return Fne

    @action(detail=True, methods=['post'], name="Add attachment")
    def add_attachment(self, request, uuid=None):
        instance = self.get_object()
        validate_uploaded_file_size(request.data['file'])
        author = request.user if request.user.is_authenticated else None
        Attachment.objects.create(
            parent=instance, author=author, **request.data)
        instance.refresh_from_db()
        return self._respond_instance(instance)


class DraftFneViewSet(FneModelMixin, DraftViewMixin, viewsets.GenericViewSet):
    ''' Brouillons de FNE
    /api/fne/draft/{uuid}/ pour accéder à un brouillon
    Les utilisateurs non authentifiés peuvent créer et mettre à jour les brouillons. Ils peuvent accéder à un brouillon donné grâce à son UUID mais ils ne peuvent pas lister l'ensemble des brouillons (pour maintenir autant que possible l'anonymat).'''
    queryset = Fne.objects.filter(status__is_draft=True)
    permission_classes = [FneActivated, AllowAny]


class FneViewSet(FneModelMixin, InvestigatorViewMixin, viewsets.ModelViewSet):
    '''
    FNE en cours de traitement.
    /api/fne/form/{uuid}/ pour accéder à un formulaire donné
    Les utilisateurs authentifiés ont accès aux formulaires qui leur sont attribués.
    '''
    queryset = Fne.objects.all()
    permission_classes = [FneActivated, GroupRestricted]
    serializer_class = FneWithSubDataSerializer
    search_fields = InvestigatorViewMixin.search_fields + \
        ['lieu', 'description', 'aircrafts__callsign',
            'cds_report__com_cds', 'sub_data__inca_number']
    queryparams_lookup_mapping = {
        'type': 'event_types__name__contains',
        **InvestigatorViewMixin.queryparams_lookup_mapping}
    safetycube_formatter_class = FneFormatter

    def get_postit_parent(self, instance):
        try:
            return instance.sub_data
        except ObjectDoesNotExist:
            return SubData.objects.create(parent_fne=instance)

    def get_postit_model(self):
        return PostIt

    def _organize_attachments(self, instance):
        images = []
        attachments = []
        for a in instance.attachments.all():
            try:
                img = Image.open(a.file)
                img.verify()
                images.append(encode_image(a.file))
            except:
                attachments.append(a.file)
        return images, attachments

    def get_export_context(self, request):
        context = super().get_export_context(request)
        instance = self.get_object()
        images, _ = self._organize_attachments(instance)
        context.update({
            'form': instance,
            'encoded_strips': [
                encode_image(a.strip)
                for a in instance.aircrafts.all()
            ],
            'encoded_drawing': encode_image(instance.drawing) if instance.drawing else None,
            'encoded_attachments': images
        })
        return context

    @action(detail=True, methods=['get'], name="Export as PDF")
    def export(self, request, uuid=None):
        instance = self.get_object()
        _, attachments = self._organize_attachments(instance)
        if len(attachments) == 0:
            return super().export(request, uuid=uuid)
        else:
            instance = self.get_object()
            context = self.get_export_context(request)
            filename = self._make_export_filename(instance)
            return self._export_as_zip(context, request, filename,
                                       attachments)


class PostItViewSet(RootViewMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
    Post-its associés à une FNE (pour mise à jour uniquement).
    /api/fne/postit/{pk}/ pour accéder à un postit donné.
    '''
    queryset = PostIt.objects.all()
    serializer_class = FnePostItSerializer
    permission_classes = [FneActivated, IsOwner]


class AttachmentViewSet(RootViewMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
    Pièces jointes associées à une FNE (pour suppression uniquement)
    /api/fne/attachment/{pk}/ pour accéder à une pièce jointe donnée.
    '''
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [FneActivated, IsOwner]
