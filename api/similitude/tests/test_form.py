from rest_framework import status
from django.contrib.auth.models import Group
from django.utils import timezone


from api.tests.base import *
from .utils import create_similitude
from shared.models.form import Status
from similitude.views import SimiViewSet
from similitude.models import Simi


class SimiFormTest(ApiTestCase):
    url = "/api/similitude/form/"

    def setUp(self):
        super().setUp()
        self.waiting = Status.objects.filter(is_waiting=True).first()
        self.done = Status.objects.filter(is_done=True).first()
        self.to_be_deleted = Status.objects.filter(
            is_to_be_deleted=True).first()
        self.etu_group = Group.objects.get(name="Sub Etudes")
        self.qse_group = Group.objects.get(name="QSS Enquête")
        self.simi = create_similitude(
            {'status': self.waiting, 'assigned_to_group': self.etu_group})

    def test_provide_subdata_on_creation(self):
        '''form can be created with sub_data'''
        request = self.factory.post(
            self.url,
            {'status': self.waiting,
             'assigned_to_group': self.qse_group,
             'description': "Il s'est passé des trucs.",
             'event_date': timezone.now(),
             'sub_data.inca_number': '123456'},
            format="multipart")
        force_authenticate(request, user=self.qss_user)
        response = SimiViewSet.as_view(actions={"post": "create"})(request)
        self.assertTrue(status.is_success(response.status_code))
        uuid = response.data['uuid']
        self.assertEqual(Simi.objects.get(
            uuid=uuid).sub_data.inca_number, "123456")

    def test_update_subdata(self):
        '''form sub_data can be updated'''
        request = self.factory.put(
            '{}{}/'.format(self.url, self.simi.uuid),
            {'status': self.waiting,
             'assigned_to_group': self.qse_group,
             'description': "Il s'est passé des trucs.",
             'event_date': timezone.now(),
             'sub_data.inca_number': 'abcde'},
            format="multipart")
        force_authenticate(request, self.qss_user)
        response = SimiViewSet.as_view({'put': 'update'})(
            request, uuid=self.simi.uuid)
        self.assertTrue(status.is_success(response.status_code))
        self.simi.refresh_from_db()
        self.assertEqual(self.simi.sub_data.inca_number, "abcde")

    def test_delete_subdata(self):
        '''form sub_data can be deleted'''
        request = self.factory.put(
            '{}{}/'.format(self.url, self.simi.uuid),
            {'status': self.waiting,
             'assigned_to_group': self.qse_group,
             'event_date': timezone.now(),
             'description': "Il s'est passé des trucs."},
            format="multipart")
        force_authenticate(request, self.qss_user)
        response = SimiViewSet.as_view({'put': 'update'})(
            request, uuid=self.simi.uuid)
        self.assertTrue(status.is_success(response.status_code))
        self.simi.refresh_from_db()
        self.assertFalse(hasattr(self.simi, 'sub_data'))
