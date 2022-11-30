from rest_framework import status
from django.contrib.auth.models import Group
from datetime import datetime
from django.utils.timezone import make_aware

from api.tests.base import *
from .utils import create_brouillage
from shared.models.form import Status
from brouillage.views import BrouillageViewSet


class BrouillageExportTest(ApiTestCase):
    url = "/api/brouillage/form/{}/export/"

    def setUp(self):
        super().setUp()
        etu_group = Group.objects.get(name="Sub Etudes")
        waiting = Status.objects.filter(is_waiting=True).first()
        self.brouillage = create_brouillage(
            {'event_date': make_aware(datetime(2022, 1, 1, 15, 30)), 'status': waiting, 'assigned_to_group': etu_group})

    def _export(self, uuid, options={}):
        request = self.factory.get(
            self.url.format(uuid), options, format="multipart")
        force_authenticate(request, self.etu_user)
        return BrouillageViewSet.as_view(
            actions={"get": "export"}, detail=True)(request, uuid=uuid)

    def test_normal_export(self):
        '''endpoint should return PDF named with event_date'''
        response = self._export(self.brouillage.uuid)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.headers['Content-Type'], "application/pdf")
        self.assertIn('filename="eBrouillage-20220101-1530.pdf"',
                      response.headers['Content-Disposition'])
