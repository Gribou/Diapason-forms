from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from constance import config
from collections import OrderedDict
from functools import reduce

from shared.email import send_mail
from shared.parsers import NestedMultipartParser
from .models import CustomForm, FormCategory
from .serializers import CustomFormSerializer, FormCategorySerializer
from .validate import validate


class CustomFormViewSet(viewsets.ReadOnlyModelViewSet):
    '''Formulaires personnalisés créés par l'administrateur
    /api/custom/form/{slug}/ pour accéder à un formulaire donné.
    '''
    queryset = CustomForm.objects.filter(enabled=True)
    serializer_class = CustomFormSerializer
    parser_classes = [NestedMultipartParser]
    lookup_field = "slug"

    @action(detail=True, methods=['post'], name="Submit a form entry")
    def submit(self, request, slug=None):
        form = self.get_object()
        clean_data, files, errors = validate(request.data, form)
        if errors is not None:
            return Response(errors,
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            if form.send_email_to is not None:
                return self._send_data_by_mail(clean_data, files, form)
            return Response({'non_field_errors': "Ce formulaire a été mal configuré. Veuillez contacter l'administrateur."}, status=status.HTTP_400_BAD_REQUEST)

    def _send_data_by_mail(self, clean_data, files, form):
        context = {
            'data': self._sort_by_fields(clean_data),
            'site_name': config.WEBSITE_NAME,
        }
        to = form.send_email_to if '@' in form.send_email_to \
            else clean_data.get(form.send_email_to, {}).get('value', None)
        if to is None:
            return Response({
                'non_field_errors': "Ce formulaire n'a pu être transmis : destination inconnue"
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            send_mail(
                context, form.title, "custom/emails/data.html",
                "custom/emails/data.txt", [to], files=files)
            return Response(
                {
                    'success': "Votre formulaire a été transmis par e-mail",
                    **{key: item['value'] for key, item in clean_data.items() if not item['is_file']}
                })
        except Exception as e:
            return Response(
                {'non_field_errors':
                    "L'envoi par e-mail a échoué ({}).".format(e)},
                status=status.HTTP_400_BAD_REQUEST)

    def _sort_by_fields(self, clean_data):
        return OrderedDict(sorted(clean_data.items(), key=lambda f: f[0]))


class FormCategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''Les formulaires sont organisés en catégories.'''
    queryset = FormCategory.objects.all()
    serializer_class = FormCategorySerializer

    def get_queryset(self):
        # return only categories relevant for this user
        if self.request.user.is_authenticated:
            return super().get_queryset().filter(Q(show_to_groups__in=self.request.user.groups.all()) | Q(show_to_groups=None)).distinct()
        else:
            return super().get_queryset().filter(show_to_groups=None)
