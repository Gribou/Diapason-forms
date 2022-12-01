from rest_framework import status
from django.contrib.auth.models import Group
from datetime import datetime
from django.utils.timezone import make_aware
from constance.test import override_config
from zipfile import ZipFile
import io

from shared.safetycube.utils import is_safetycube_enabled

from api.tests.base import *
from api.tests.utils import generate_uploaded_any_file, generate_uploaded_photo_file
from .utils import create_fne
from shared.models.form import Status
from efne.models import Attachment
from efne.views import FneViewSet
from shared.models.form import SafetyCubeRef


class FneExportTest(ApiTestCase):
    url = "/api/fne/form/{}/export/"

    def setUp(self):
        super().setUp()
        qse_group = Group.objects.get(name="QSS Enquête")
        waiting = Status.objects.filter(is_waiting=True).first()
        self.fne = create_fne(
            {'event_date': make_aware(datetime(2022, 1, 1, 15, 30)), 'status': waiting, 'assigned_to_group': qse_group})

    def _export(self, uuid, options={}):
        request = self.factory.get(
            self.url.format(uuid), options, format="multipart")
        force_authenticate(request, self.qss_user)
        return FneViewSet.as_view(
            actions={"get": "export"}, detail=True)(request, uuid=uuid)

    def test_normal_export(self):
        '''endpoint should return PDF named with event_date'''
        response = self._export(self.fne.uuid)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.headers['Content-Type'], "application/pdf")
        self.assertIn('filename="eFNE-20220101-1530.pdf"',
                      response.headers['Content-Disposition'])
        self.assertTrue(response.content)  # check that response is not empty

    def test_anonymous_export(self):
        '''endpoint should accept 'anonymous' params'''
        response = self._export(self.fne.uuid, {'anonymous': 'true'})
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.headers['Content-Type'], "application/pdf")

    @override_config(DB_TYPE="SAFETYCUBE", SAFETYCUBE_USERNAME="diapason")
    def test_export_with_safetycube_reference(self):
        '''exported file should be named with safetycube ref if provided'''
        self.fne.safetycube = SafetyCubeRef.objects.create(reference="FF5678")
        self.fne.save()
        response = self._export(self.fne.uuid)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.headers['Content-Type'], "application/pdf")
        self.assertIn('filename="eFNE-FF5678.pdf"',
                      response.headers['Content-Disposition'])

    def test_export_with_images_attachments(self):
        '''exported file should be a pdf if all attachments are images'''
        Attachment.objects.create(
            parent=self.fne, file=generate_uploaded_photo_file())
        response = self._export(self.fne.uuid)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.headers['Content-Type'], "application/pdf")

    def test_export_with_file_attachments(self):
        '''exported file should be a zip if an attachment is not an image'''
        file = generate_uploaded_any_file()
        Attachment.objects.create(parent=self.fne, file=file)
        response = self._export(self.fne.uuid)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(
            response.headers['Content-Type'], "application/x-zip-compressed")
        self.assertIn('filename="eFNE-20220101-1530.zip"',
                      response.headers['Content-Disposition'])
        z = ZipFile(io.BytesIO(response.content))
        self.assertIn('eFNE-20220101-1530/test.txt', z.namelist())
        self.assertIn(
            'eFNE-20220101-1530/eFNE-20220101-1530.pdf', z.namelist())
