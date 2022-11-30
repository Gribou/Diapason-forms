
from rest_framework import status
from django.test import override_settings

from api.tests.base import *
from api.tests.utils import generate_uploaded_any_file
from .utils import create_fne

from efne.models import Attachment
from efne.views import FneViewSet, DraftFneViewSet, AttachmentViewSet


class FneAttachmentTest(ApiTestCase):
    url = "/api/fne/attachment/"
    form_url = "/api/fne/form/{}/add_attachment/"
    draft_url = "/api/fne/draft/{}/add_attachment/"

    def test_add_attachment_anonymously(self):
        '''endpoint should add attachment to form'''
        fne = create_fne({})
        request = self.factory.post(
            self.draft_url.format(fne.uuid), {'file': generate_uploaded_any_file()}, format="multipart")
        response = DraftFneViewSet.as_view(
            actions={"post": "add_attachment"}, detail=True)(request, uuid=fne.uuid)
        self.assertTrue(status.is_success(response.status_code))
        fne.refresh_from_db()
        self.assertEqual(fne.attachments.count(), 1)
        self.assertTrue(fne.attachments.first().file.name.endswith("test.txt"))
        self.assertIsNone(fne.attachments.first().author)

    def test_add_attachment_with_author(self):
        '''endpoint should set author according to authenticated user'''
        fne = create_fne({})
        request = self.factory.post(
            self.form_url.format(fne.uuid), {'file': generate_uploaded_any_file()}, format="multipart")
        force_authenticate(request, self.qss_user)
        response = FneViewSet.as_view(
            actions={"post": "add_attachment"}, detail=True)(request, uuid=fne.uuid)
        self.assertTrue(status.is_success(response.status_code))
        fne.refresh_from_db()
        self.assertEqual(fne.attachments.first().author, self.qss_user)

    def test_attachment_list_is_not_reachable(self):
        '''endpoint should not answer to list requests'''
        fne = create_fne({})
        Attachment.objects.create(
            parent=fne, file=generate_uploaded_any_file())
        Attachment.objects.create(
            parent=fne, file=generate_uploaded_any_file())
        request = self.factory.get(self.url)
        force_authenticate(request, self.qss_user)
        response = AttachmentViewSet.as_view(actions={'get': 'list'})(request)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_destroy_attachment_if_is_owner(self):
        '''endpoint should delete attachment object if is owner'''
        fne = create_fne({})
        att = Attachment.objects.create(
            parent=fne, file=generate_uploaded_any_file(), author=self.etu_user)
        request = self.factory.delete("{}{}/".format(self.url, att.pk))
        force_authenticate(request, self.etu_user)
        response = AttachmentViewSet.as_view(
            actions={'delete': 'destroy'})(request, pk=att.pk)
        self.assertTrue(status.is_success(response.status_code))
        self.assertFalse(Attachment.objects.filter(pk=att.pk).exists())

    def test_do_not_destroy_attachment_if_not_owner(self):
        '''endpoint should not delete attachment object if not owner'''
        fne = create_fne({})
        att = Attachment.objects.create(
            parent=fne, file=generate_uploaded_any_file())
        request = self.factory.delete("{}{}/".format(self.url, att.pk))
        force_authenticate(request, self.etu_user)
        response = AttachmentViewSet.as_view(
            actions={'delete': 'destroy'})(request, pk=att.pk)
        self.assertTrue(status.is_client_error(response.status_code))
        self.assertTrue(Attachment.objects.filter(pk=att.pk).exists())
