from rest_framework import status
from django.contrib.auth.models import Group
from datetime import datetime
from django.utils.timezone import make_aware
from constance.test import override_config

from api.tests.base import *
from .utils import create_similitude
from shared.models.form import Status
from similitude.models import SubData
from similitude.views import SimiViewSet


class SimiExportTest(ApiTestCase):
    url = "/api/similitude/form/{}/export/"

    def setUp(self):
        super().setUp()
        qse_group = Group.objects.get(name="QSS Enquête")
        waiting = Status.objects.filter(is_waiting=True).first()
        self.simi = create_similitude(
            {'event_date': make_aware(datetime(2022, 1, 1, 15, 30)), 'status': waiting, 'assigned_to_group': qse_group})

    def _export(self, uuid, options={}):
        request = self.factory.get(
            self.url.format(uuid), options, format="multipart")
        force_authenticate(request, self.qss_user)
        return SimiViewSet.as_view(
            actions={"get": "export"}, detail=True)(request, uuid=uuid)

    def test_normal_export(self):
        '''endpoint should return PDF named with event_date'''
        response = self._export(self.simi.uuid)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.headers['Content-Type'], "application/pdf")
        self.assertIn('filename="eSimilitude-20220101-1530.pdf"',
                      response.headers['Content-Disposition'])

    @override_config(DB_TYPE="INCA", SAFETYCUBE_USERNAME="diapason")
    def test_export_with_inca_number(self):
        '''exported file should be named with inca number if provided'''
        SubData.objects.create(parent_simi=self.simi, inca_number="FF5678")
        response = self._export(self.simi.uuid)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.headers['Content-Type'], "application/pdf")
        self.assertIn('filename="eSimilitude-FF5678.pdf"',
                      response.headers['Content-Disposition'])
