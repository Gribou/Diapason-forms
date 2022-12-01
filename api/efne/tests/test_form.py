from rest_framework import status
from django.contrib.auth.models import Group
from constance.test import override_config
from django.utils import timezone
from datetime import timedelta


from api.tests.base import *
from .utils import create_fne
from shared.models.form import Status
from efne.views import FneViewSet
from efne.models import Fne


class FneFormTest(ApiTestCase):
    url = "/api/fne/form/"

    def setUp(self):
        super().setUp()
        self.waiting = Status.objects.filter(is_waiting=True).first()
        self.done = Status.objects.filter(is_done=True).first()
        self.to_be_deleted = Status.objects.filter(
            is_to_be_deleted=True).first()
        self.etu_group = Group.objects.get(name="Sub Etudes")
        self.qse_group = Group.objects.get(name="QSS Enquête")
        self.fne = create_fne(
            {'status': self.waiting, 'assigned_to_group': self.etu_group})

    def test_read_anonymous(self):
        '''endpoint should forbid access if not authenticated'''
        request = self.factory.get('{}{}'.format(self.url, self.fne.uuid))
        response = FneViewSet.as_view({"get": "retrieve"})(
            request, uuid=self.fne.uuid)
        self.assertTrue(status.is_client_error(response.status_code))

    @override_config(SHOW_FNE=False)
    def test_read_feature_disabled(self):
        '''endpoint should forbid access if feature is deactivated'''
        request = self.factory.get('{}{}'.format(self.url, self.fne.uuid))
        force_authenticate(request, self.qss_user)
        response = FneViewSet.as_view({"get": "retrieve"})(
            request, uuid=self.fne.uuid)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_read_assigned_form(self):
        '''endpoint should authorize access to assigned forms'''
        request = self.factory.get('{}{}'.format(self.url, self.fne.uuid))
        force_authenticate(request, self.etu_user)
        response = FneViewSet.as_view({"get": "retrieve"})(
            request, uuid=self.fne.uuid)
        self.assertTrue(status.is_success(response.status_code))
        self.assertIn('sub_data', response.data)

        other_fne = create_fne(
            {'status': self.waiting, 'assigned_to_group': self.qse_group})
        request = self.factory.get('{}{}'.format(self.url, other_fne.uuid))
        force_authenticate(request, self.etu_user)
        response = FneViewSet.as_view({"get": "retrieve"})(
            request, uuid=other_fne.uuid)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_read_all_access(self):
        '''endpoint should authorize access to all validated forms to all access user'''
        request = self.factory.get('{}{}'.format(self.url, self.fne.uuid))
        force_authenticate(request, self.qss_user)
        response = FneViewSet.as_view({"get": "retrieve"})(
            request, uuid=self.fne.uuid)
        self.assertTrue(status.is_success(response.status_code))

    def test_apply_available_action(self):
        '''endpoint should make form progress to next status if action exists in graph'''
        fne = create_fne(
            {'status': self.waiting, 'assigned_to_group': self.etu_group})
        request = self.factory.put(
            '{}{}/apply_action/'.format(self.url, fne.uuid), {'next_status': self.done.pk, 'next_group': self.qse_group.pk}, format="multipart")
        force_authenticate(request, self.etu_user)
        response = FneViewSet.as_view(
            {'put': 'apply_action'})(request, uuid=fne.uuid)
        self.assertTrue(status.is_success(response.status_code))
        fne.refresh_from_db()
        self.assertTrue(fne.status.is_done)

    def test_apply_not_available_action(self):
        '''endpoint should raise error if action is not available'''
        fne = create_fne(
            {'status': self.waiting, 'assigned_to_group': self.etu_group})
        request = self.factory.put(
            '{}{}/apply_action/'.format(self.url, fne.uuid), {'next_status': self.to_be_deleted.pk, 'next_group': self.etu_group.pk}, format="multipart")
        force_authenticate(request, self.etu_user)
        response = FneViewSet.as_view(
            {'put': 'apply_action'})(request, uuid=fne.uuid)
        self.assertTrue(status.is_client_error(response.status_code))
        self.assertTrue(fne.status.is_waiting)

    def test_apply_default_action(self):
        '''endpoint should make form progress to next status'''
        cds_group = Group.objects.get(name="Chef de Salle")
        fne = create_fne({'status': self.done, 'assigned_to_group': cds_group})
        request = self.factory.put(
            '{}{}/apply_action/'.format(self.url, fne.uuid), format="multipart")
        force_authenticate(request, self.cds_user)
        response = FneViewSet.as_view(
            {'put': 'apply_action'})(request, uuid=fne.uuid)
        self.assertTrue(status.is_success(response.status_code))
        fne.refresh_from_db()
        self.assertTrue(fne.status.is_waiting)
        self.assertEqual(fne.assigned_to_group, self.qse_group)

    def test_apply_default_action_when_none_exists(self):
        '''endpoint should raise error if default action is not available'''
        fne = create_fne(
            {'status': self.waiting, 'assigned_to_group': self.qse_group})
        request = self.factory.put(
            '{}{}/apply_action/'.format(self.url, fne.uuid), format="multipart")
        force_authenticate(request, self.qss_user)
        response = FneViewSet.as_view(
            {'put': 'apply_action'})(request, uuid=fne.uuid)
        self.assertTrue(status.is_client_error(response.status_code))
        self.assertTrue(fne.status.is_waiting)
        self.assertEqual(fne.assigned_to_group, self.qse_group)

    def test_assign_to_person(self):
        '''endpoint should change assigned_to_person value'''
        request = self.factory.put(
            '{}{}/assign_to_person/'.format(self.url, self.fne.uuid), {'next_person': "MOI"}, format="multipart")
        force_authenticate(request, self.etu_user)
        response = FneViewSet.as_view(
            {'put': 'assign_to_person'})(request, uuid=self.fne.uuid)
        self.assertTrue(status.is_success(response.status_code))
        self.fne.refresh_from_db()
        self.assertEqual(self.fne.assigned_to_person, "MOI")

        request = self.factory.put(
            '{}{}/assign_to_person/'.format(self.url, self.fne.uuid), {}, format="multipart")
        force_authenticate(request, self.etu_user)
        response = FneViewSet.as_view(
            {'put': 'assign_to_person'})(request, uuid=self.fne.uuid)
        self.assertTrue(status.is_success(response.status_code))
        self.fne.refresh_from_db()
        self.assertIsNone(self.fne.assigned_to_person)

    def test_keywords(self):
        '''endpoint should change keywords value'''
        request = self.factory.put(
            '{}{}/keywords/'.format(self.url, self.fne.uuid), {'keywords': "4F FRA"}, format="multipart")
        force_authenticate(request, self.etu_user)
        response = FneViewSet.as_view(
            {'put': 'keywords'})(request, uuid=self.fne.uuid)
        self.assertTrue(status.is_success(response.status_code))
        self.fne.refresh_from_db()
        self.assertEqual(self.fne.keywords, "4F FRA")

        request = self.factory.put(
            '{}{}/keywords/'.format(self.url, self.fne.uuid), {}, format="multipart")
        force_authenticate(request, self.etu_user)
        response = FneViewSet.as_view(
            {'put': 'keywords'})(request, uuid=self.fne.uuid)
        self.assertTrue(status.is_success(response.status_code))
        self.fne.refresh_from_db()
        self.assertIsNone(self.fne.keywords)

    def test_warnings_and_alarms(self):
        fne = create_fne(
            {'status': self.waiting, 'assigned_to_group': self.qse_group, 'event_date': timezone.now() - timedelta(days=3),
             'sub_data': {'is_safety_event': True}, })
        request = self.factory.get('{}{}/'.format(self.url, fne.uuid))
        force_authenticate(request, self.qss_user)
        response = FneViewSet.as_view({"get": "retrieve"})(
            request, uuid=fne.uuid)
        self.assertFalse(response.data['has_warning'])
        self.assertFalse(response.data['has_alarm'])

        fne2 = create_fne(
            {'status': self.waiting, 'assigned_to_group': self.qse_group, 'event_date': timezone.now() - timedelta(days=70),
             'sub_data': {'is_safety_event': True}, })
        request = self.factory.get('{}{}/'.format(self.url, fne2.uuid))
        force_authenticate(request, self.qss_user)
        response = FneViewSet.as_view({"get": "retrieve"})(
            request, uuid=fne2.uuid)
        self.assertTrue(response.data['has_warning'])
        self.assertFalse(response.data['has_alarm'])

        fne3 = create_fne(
            {'status': self.waiting, 'assigned_to_group': self.qse_group, 'event_date': timezone.now() - timedelta(days=90),
             'sub_data': {'is_safety_event': True}, })
        request = self.factory.get('{}{}/'.format(self.url, fne3.uuid))
        force_authenticate(request, self.qss_user)
        response = FneViewSet.as_view({"get": "retrieve"})(
            request, uuid=fne3.uuid)
        self.assertFalse(response.data['has_warning'])
        self.assertTrue(response.data['has_alarm'])

    def test_provide_subdata_on_creation(self):
        '''form can be created with sub_data'''
        # TODO test with safetycube instead
        request = self.factory.post(
            self.url,
            {'status': self.waiting,
             'assigned_to_group': self.qse_group,
             'description': "Il s'est passé des trucs.",
             'event_date': timezone.now(),
             'position': "AA",
             'regroupement': 'ZZZZ',
             'sub_data.inca_number': '123456'},
            format="multipart")
        force_authenticate(request, user=self.qss_user)
        response = FneViewSet.as_view(actions={"post": "create"})(request)
        self.assertTrue(status.is_success(response.status_code))
        uuid = response.data['uuid']
        self.assertEqual(Fne.objects.get(
            uuid=uuid).sub_data.inca_number, "123456")

    def test_update_subdata(self):
        '''form sub_data can be updated'''
        # TODO test with safetycube instead
        request = self.factory.put(
            '{}{}/'.format(self.url, self.fne.uuid),
            {'status': self.waiting,
             'assigned_to_group': self.qse_group,
             'description': "Il s'est passé des trucs.",
             'event_date': timezone.now(),
             'position': "AA",
             'regroupement': 'ZZZZ',
             'sub_data.inca_number': 'abcde'},
            format="multipart")
        force_authenticate(request, self.qss_user)
        response = FneViewSet.as_view({'put': 'update'})(
            request, uuid=self.fne.uuid)
        self.assertTrue(status.is_success(response.status_code))
        self.fne.refresh_from_db()
        self.assertEqual(self.fne.sub_data.inca_number, "abcde")

    def test_delete_subdata(self):
        '''form sub_data can be deleted'''
        request = self.factory.put(
            '{}{}/'.format(self.url, self.fne.uuid),
            {'status': self.waiting,
             'assigned_to_group': self.qse_group,
             'description': "Il s'est passé des trucs.",
             'event_date': timezone.now(),
             'position': "AA",
             'regroupement': 'ZZZZ'},
            format="multipart")
        force_authenticate(request, self.qss_user)
        response = FneViewSet.as_view({'put': 'update'})(
            request, uuid=self.fne.uuid)
        self.assertTrue(status.is_success(response.status_code))
        self.fne.refresh_from_db()
        self.assertFalse(hasattr(self.fne, 'sub_data'))
