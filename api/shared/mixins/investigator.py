from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import PermissionDenied
from rest_framework.status import HTTP_204_NO_CONTENT
from django.db.models import F, Q
from django.core.exceptions import ObjectDoesNotExist
from constance import config
import traceback

from ..pagination import CustomPageNumberPagination
from ..export import render_response_as_pdf, render_file_as_pdf, render_response_as_zip
from ..models.config import user_has_all_access
from ..safetycube.utils import send_to_safetycube, refresh_safetycube_status
from ..tasks import send_all_to_safetycube
from ..answer import send_answer_to_redactors, remember_redactors


class ExportViewMixin:

    def get_export_context(self, request):
        return {
            'anonymous': request.query_params.get(
                'anonymous', False) == 'true',
            'pdf_export_header': config.PDF_EXPORT_HEADER,
            'safetycube_enabled': self.get_model().options.is_safetycube_enabled(),
            'title': self.get_model().options.short_form_name,
            'full_form_name': self.get_model().options.long_form_name
        }

    def _get_export_template(self):
        return "{}/export/pdf.html".format(self.get_model()._meta.app_label)

    def _make_export_filename(self, instance):
        prefix = "e{}".format(instance.options.short_form_name)
        try:
            if instance.options.is_safetycube_enabled():
                if instance.safetycube and instance.safetycube.reference:
                    return "{}-{}".format(
                        prefix,
                        instance.safetycube.reference)
            if instance.sub_data.inca_number:
                return "{}-{}".format(
                    prefix,
                    instance.sub_data.inca_number)
        except (ObjectDoesNotExist, AttributeError):
            pass
        return instance.event_date.strftime("{}-%Y%m%d-%H%M".format(prefix))

    def _export_as_pdf(self, context, request, filename):
        return render_response_as_pdf(self._get_export_template(), context, request, filename)

    def _export_as_zip(self, context, request, filename,
                       attachments):
        doc = render_file_as_pdf(self._get_export_template(), context, request)
        doc.name = "{}.pdf".format(filename)
        attachments.append(doc)
        return render_response_as_zip(attachments, filename)

    @action(detail=True, methods=['get'], name="Export as PDF")
    def export(self, request, uuid=None,):
        instance = self.get_object()
        context = self.get_export_context(request)
        filename = self._make_export_filename(instance)
        return self._export_as_pdf(context, request, filename)


class PostitMixin:

    @action(detail=True, methods=['post'], name="Add a postit")
    def add_postit(self, request, uuid=None):
        instance = self.get_object()
        postit_parent = self.get_postit_parent(instance)
        self.get_postit_model().objects.create(parent=postit_parent,
                                               author=request.user, **request.data)
        instance.refresh_from_db()
        return self._respond_instance(instance)

    def get_postit_parent(self):
        # must be implemented in view
        raise NotImplementedError()

    def get_postit_model(self):
        # must be implented in view
        raise NotImplementedError()


class SafetyCubeMixin:

    def check_safetycube_disabled(self):
        if not self.get_model().options.is_safetycube_enabled():
            raise PermissionDenied({
                'non_field_errors':
                "Les fonctionnalités SafetyCube ne sont pas activées."})

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        try:
            self.check_safetycube_disabled()
            has_safetycube_reference_lookup = self.request.query_params.get(
                "safetycube", None)
            if has_safetycube_reference_lookup is not None:
                queryset = queryset.filter(
                    safetycube__reference__isnull=has_safetycube_reference_lookup == "false")
        except:
            pass
        return queryset

    @action(detail=True, methods=['post'], name="Save to SafetyCube")
    def save_to_safetycube(self, request, uuid=None):
        self.check_safetycube_disabled()
        try:
            send_to_safetycube(uuid, self.get_model())
            return self._respond_instance(self.get_object())
        except Exception as e:
            raise ValidationError({'non_field_errors': str(e)})

    @action(detail=False, methods=['post'], name="Save all to SafetyCube")
    def save_all_to_safetycube(self, request):
        self.check_safetycube_disabled()
        try:
            uuid_list = list(super().get_queryset().filter(
                safetycube__reference__isnull=True).values_list("uuid", flat=True).all())
            send_all_to_safetycube.delay(uuid_list, self.get_model(
            )._meta.app_label, self.get_model().model.__name__)
            return Response(status=HTTP_204_NO_CONTENT)
        except Exception as e:
            raise ValidationError({'non_field_errors': str(e)})

    @action(detail=True, methods=['get'], name="Refresh status from SafetyCube")
    def refresh_safetycube_status(self, request, uuid=None):
        self.check_safetycube_disabled()
        try:
            refresh_safetycube_status(uuid, self.get_model())
            return self._respond_instance(self.get_object())
        except Exception as e:
            raise ValidationError({'non_field_errors': str(e)})


class AnswerToRedactorsMixin:

    @action(detail=True, methods=['post'], name="Send an answer by email to the redactors")
    def send_answer(self, request, uuid=None):
        self._validate_answer(request)
        try:
            send_answer_to_redactors(uuid, self.get_model(
            ), request)
            instance = self.get_object()
            instance.apply_default_action()
            remember_redactors(request.data.get("redactors", []))
            return self._respond_instance(instance)
        except Exception as e:
            traceback.print_exc()
            raise ValidationError({'non_field_errors': str(e)})

    def _validate_answer(self, request):
        instance = self.get_object()
        if not instance.status.is_done:
            raise ValidationError(
                {'non_field_errors': "Le traitement de cette fiche n'est pas terminé"})
        errors = {}
        if not any([r.get('email', None) for r in request.data.get('redactors', [])]):
            errors['non_field_errors'] = "Veuillez indiquer au moins une addresse email"
        if not request.data.get('answer', None):
            errors['answer'] = "Ce champ est obligatoire"
        if errors:
            raise ValidationError(errors)


class InvestigatorViewMixin(ExportViewMixin, AnswerToRedactorsMixin, PostitMixin, SafetyCubeMixin):
    ordering = [F('safetycube__reference').desc(nulls_first=True),
                F('sub_data__inca_number').desc(nulls_first=True), '-event_date']
    pagination_class = CustomPageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['assigned_to_person', 'keywords', 'safetycube__reference']
    queryparams_lookup_mapping = {
        "status": "status__label",
        "group": "assigned_to_group__name",
        "keywords": "keywords__contains",
        "zone": "redactors__team__zone__short_name"
    }

    def get_queryset(self):
        '''give access only to group related reports (or only validated reports for all access groups)'''
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_authenticated and user_has_all_access(user):
            queryset = queryset.exclude(
                assigned_to_group__permissions__codename='validator')
        else:
            queryset = queryset.filter(assigned_to_group__in=user.groups.all())
        return queryset

    def filter_queryset(self, queryset):
        ''' handle query params, do not show drafts or to be deleted reports'''
        # This method is called only for LIST endpoint so it does not prevent a user from reading a form by uuid
        queryset = super().filter_queryset(queryset).exclude(
            status__is_draft=True).exclude(status__is_to_be_deleted=True).distinct()
        for keyword, lookup in self.queryparams_lookup_mapping.items():
            value = self.request.query_params.get(keyword, None)
            if value is not None:
                filter = Q()
                for v in value.split(","):
                    filter = filter | Q(**{lookup: v})
                queryset = queryset.filter(filter)
        return self._sort_queryset(queryset)

    def _sort_queryset(self, queryset):
        '''order queryset by reference or event_date depending on query params'''
        sort_order = self.request.query_params.get("sort", None)
        if sort_order == "date":
            return queryset.order_by("event_date")
        if sort_order == "-date":
            return queryset.order_by("-event_date")
        if sort_order == "ref":
            return queryset.order_by(*self.ordering).reverse()
        return queryset.order_by(*self.ordering)

    @action(detail=True, methods=['put'], name="Assigned to person")
    def assign_to_person(self, request, uuid=None):
        instance = self.get_object()
        instance.assigned_to_person = request.data.get('next_person', None)
        instance.save()
        return self._respond_instance(instance)

    @action(detail=True, methods=['put'], name="Set keywords")
    def keywords(self, request, uuid=None):
        instance = self.get_object()
        instance.keywords = request.data.get('keywords', None)
        instance.save()
        return self._respond_instance(instance)
