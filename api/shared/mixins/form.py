
from rest_framework.serializers import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from ..parsers import NestedMultipartParser
from ..models.config import group_is_validator, user_has_all_access, user_is_validator


class WorkflowMixin:

    def handle_options(self, instance, options, user):
        # if proceed, apply default action once
        # if bypass_validation, apply default action again until reaching correct state
        if options.get('proceed', False) == 'true' and instance.is_default_action_available():
            instance.apply_default_action()
            instance.refresh_from_db()
            if options.get('bypass_validation', False) == 'true' and instance.is_default_action_available():
                if user_is_validator(user):
                    # apply default until status is 'done' or group is not validator
                    while group_is_validator(instance.assigned_to_group) and not instance.status.is_done and instance.is_default_action_available():
                        instance.apply_default_action()
                        instance.refresh_from_db()
                if user_has_all_access(user):
                    # TODO if is investigator instead ?
                    # apply default until group is not validator
                    while group_is_validator(instance.assigned_to_group) and instance.is_default_action_available():
                        instance.apply_default_action()
                        instance.refresh_from_db()
        return instance

    @action(detail=True, methods=['put'], name="Apply action")
    def apply_action(self, request, uuid=None):
        instance = self.get_object()
        # if action is detailed in request body, apply action
        if 'next_status' in request.data or 'next_group' in request.data:
            next_status_pk = request.data.get('next_status', None)
            next_group_pk = request.data.get('next_group', None)
            self._check_action_exists(instance, next_status_pk, next_group_pk)
            instance.apply_action_by_pk(next_status_pk, next_group_pk)
        else:
            # apply default action if exist
            instance = self.get_object()
            self._check_default_action_exists(instance)
            instance.apply_default_action()
        return self._respond_instance(instance)

    def _check_action_exists(self, instance, next_status_pk, next_group_pk):
        if not instance.is_action_available(next_status_pk, next_group_pk):
            raise ValidationError("Cette action n'est pas possible.")

    def _check_default_action_exists(self, instance):
        if not instance.is_default_action_available():
            raise ValidationError(
                "Il n'existe pas d'action par défaut dans ce cas. Veuillez fournir une action."
            )


class FormViewMixin(WorkflowMixin):
    parser_classes = [NestedMultipartParser]
    lookup_field = "uuid"

    def get_model(self):
        # return the model of the current form (needs to be implemented by class using this mixin)
        raise NotImplementedError()

    def get_object(self):
        # allow all access users to access all fnes directly (but keep list view filtered)
        return get_object_or_404(self.get_model().objects.all(), uuid=self.kwargs['uuid']) if self.request.user.is_authenticated and user_has_all_access(self.request.user) else super().get_object()
        # useful for example to let all access user bypass validation when submitting an efne directly

    def create(self, request, *args, **kwargs):
        # auto apply actions according to and options from request
        options = request.data.pop("options", {})
        response = super().create(request, *args, **kwargs)
        instance = self.get_model().objects.get(uuid=response.data.get('uuid', None))
        instance = self.handle_options(instance, options, request.user)
        return self._respond_instance(instance)

    def update(self, request, *args, **kwargs):
        # auto apply actions according to and options from request
        options = request.data.pop("options", {})
        super().update(request, *args, **kwargs)
        instance = self.get_object()
        instance = self.handle_options(instance, options, request.user)
        return self._respond_instance(instance)

    def clean_incoming_media(self, data, existing_media, media_attr, media_url_attr):
        # when no new media is sent by user, media_url is provided and we want to keep the existing file
        # when the user wants to remove the existing media, media_url is not provided
        # when the user wants to import a new media, media is provided
        # returns True if parent instance needs to be saved
        if not data.get(media_attr, None):
            if data.get(media_url_attr, None):
                data[media_attr] = existing_media
            else:
                existing_media.delete()
                existing_media = None
                return True

    def _respond_instance(self, instance):
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_serializer_context(self):
        # pass list of item uuids to serializer so that it can join previous and next form uuid to serialized form
        queryset = self.filter_queryset(self.get_queryset())
        context = super().get_serializer_context()
        context['items'] = list(queryset.values_list("uuid", flat=True).all())
        return context
