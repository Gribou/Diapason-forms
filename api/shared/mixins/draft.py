from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework import mixins
from django.urls import reverse_lazy
from constance import config

from ..email import send_mail
from ..models.form import Status


class DraftViewMixin(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        # force status to DRAFT
        serializer.save(status=Status.objects.filter(is_draft=True).first())

    def perform_update(self, serializer):
        # force status to DRAFT
        serializer.save(status=Status.objects.filter(is_draft=True).first())

    def build_draft_url(self, request, uuid):
        return "{}://{}{}{}{}".format(
            request.scheme, config.HOSTNAME, reverse_lazy("home"), self.get_model().options.detail_url_template, uuid)

    @action(detail=True, methods=['post'], name="Send link by email")
    def send_link(self, request, uuid=None):
        # send by email the url of this form for later completion
        if "to" in request.data:
            context = {
                'link': self.build_draft_url(request, uuid),
                'contact_mail': config.EMAIL_ADMIN,
                'site_name': config.WEBSITE_NAME,
                'form_name': self.get_model().options.short_form_name
            }
            send_mail(
                context, "Votre brouillon de {}".format(
                    self.get_model().options.short_form_name), "shared/emails/draft_link.html",
                "shared/emails/draft_link.txt", [request.data['to']])
        return self._respond_instance(self.get_object())
