from rest_framework import status
from django.contrib.auth.models import Group
from django.utils import timezone
from datetime import timedelta

from .base import *
from shared.models.config import Team
from shared.models.form import Status
from efne.models import EventType, Role
from api.views import FormsMetaViewSet
from efne.tests.utils import create_fne
from brouillage.tests.utils import create_brouillage
from similitude.tests.utils import create_similitude


class ListMetaTest(ApiTestCase):
    '''Meta endpoints computes forms count and available filters for the forms attributed to the authenticated user
    'All access' users have access to all validated forms    
    '''

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        waiting = Status.objects.filter(is_waiting=True).first()
        in_progress = Status.objects.filter(is_in_progress=True).first()
        cds_group = Group.objects.get(name="Chef de Salle")
        etu_group = Group.objects.get(name="Sub Etudes")
        qse_group = Group.objects.get(name="QSS Enquête")
        eventtype1 = EventType.objects.get(name="ATFM")
        eventtype2 = EventType.objects.get(name="TCAS")
        eventtype3 = EventType.objects.get(name="Coflight")
        west_team = Team.objects.filter(zone__short_name="W").first()
        east_team = Team.objects.filter(zone__short_name="E").first()
        any_role = Role.objects.first()
        create_fne({
            'status': waiting, 'assigned_to_group': cds_group,
            'event_types': [eventtype3],
            'keywords': 'CDS'
        })
        create_fne({
            'status': waiting, 'assigned_to_group': qse_group,
            'event_types': [eventtype1, eventtype2],
            'keywords': 'Test',
            'event_date': timezone.now() - timedelta(days=90),
            'sub_data': {'is_safety_event': True},
            'redactors': [{'fullname': 'Fullname', 'role': any_role, 'team': east_team}]
        })
        create_fne({
            'status': in_progress, 'assigned_to_group': qse_group, 'event_types': [],
            'keywords': '4F Test',
            'event_date': timezone.now() - timedelta(days=3),
            'sub_data': {'is_safety_event': True},
            'redactors': [{'fullname': 'Fullname', 'role': any_role, 'team': east_team}]
        })
        create_fne({
            'status': waiting, 'assigned_to_group': etu_group,
            'event_types': [eventtype1],
            'keywords': '4F',
            'event_date': timezone.now() - timedelta(days=70),
            'sub_data': {'is_safety_event': True},
            'redactors': [{'fullname': 'Fullname', 'role': any_role, 'team': west_team}]
        })
        create_similitude(
            {'status': waiting, 'assigned_to_group': cds_group, 'keywords': 'CDS'})
        create_similitude({
            'status': waiting, 'assigned_to_group': qse_group, 'keywords': 'Test',
            'redactors': [
                {'fullname': 'Fullname', 'team': east_team},
                {'fullname': 'Fullname', 'team': west_team}
            ]
        })
        create_similitude({
            'status': in_progress, 'assigned_to_group': qse_group,
            'keywords': '4F Test',
            'redactors': [
                {'fullname': 'Fullname', 'team': east_team}
            ]
        })
        create_brouillage({
            'status': waiting, 'assigned_to_group': cds_group,
            'keywords': 'CDS'
        })
        create_brouillage({
            'status': in_progress, 'assigned_to_group': etu_group, 'keywords': '4F Test',
            'redactors': [
                {'fullname': 'Fullname', 'team': east_team},
                {'fullname': 'Fullname', 'team': west_team}
            ]
        })
        create_brouillage({
            'status': waiting, 'assigned_to_group': etu_group, 'keywords': 'Test',
            'redactors': [
                {'fullname': 'Fullname', 'team': east_team}
            ]
        })

    def _get(self, user=None):
        request = self.factory.get("/api/meta/")
        if user:
            force_authenticate(request, user=user)
        return FormsMetaViewSet.as_view(actions={'get': 'list'})(request)

    def test_anonymous_user(self):
        '''403 if user is not authenticated'''
        response = self._get()
        self.assertTrue(status.is_client_error(response.status_code))

    def test_normal_user(self):
        '''Metadata should be empty when user is not in any relevant group'''
        response = self._get(user=self.normal_user)
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue(response.data['empty'])
        self.assertFalse(response.data['forms']['fne']['relevant'])
        self.assertFalse(response.data['forms']['brouillage']['relevant'])
        self.assertFalse(response.data['forms']['similitude']['relevant'])
        self.assertEqual(response.data['forms']['fne']['count'], 0)
        self.assertEqual(response.data['forms']['brouillage']['count'], 0)
        self.assertEqual(response.data['forms']['similitude']['count'], 0)

    def test_validator(self):
        '''counts and relevance is correct when user is validator'''
        response = self._get(user=self.cds_user)
        self.assertTrue(status.is_success(response.status_code))
        self.assertFalse(response.data['empty'])
        self.assertTrue(response.data['forms']['fne']['relevant'])
        self.assertTrue(response.data['forms']['brouillage']['relevant'])
        self.assertTrue(response.data['forms']['similitude']['relevant'])
        self.assertEqual(response.data['forms']['fne']['count'], 1)
        self.assertEqual(response.data['forms']['brouillage']['count'], 1)
        self.assertEqual(response.data['forms']['similitude']['count'], 1)

    def test_investigator(self):
        '''counts and relevance is correct when user is investigator'''
        response = self._get(user=self.etu_user)
        self.assertTrue(status.is_success(response.status_code))
        self.assertFalse(response.data['empty'])
        self.assertTrue(response.data['forms']['fne']['relevant'])
        self.assertTrue(response.data['forms']['brouillage']['relevant'])
        self.assertFalse(response.data['forms']['similitude']['relevant'])
        self.assertEqual(response.data['forms']['fne']['count'], 1)
        self.assertEqual(response.data['forms']['brouillage']['count'], 2)
        self.assertEqual(response.data['forms']['similitude']['count'], 0)

    def test_all_access(self):
        '''counts and relevance is correct when user has all access'''
        response = self._get(user=self.qss_user)
        self.assertTrue(status.is_success(response.status_code))
        self.assertFalse(response.data['empty'])
        self.assertTrue(response.data['forms']['fne']['relevant'])
        self.assertFalse(response.data['forms']['brouillage']['relevant'])
        self.assertTrue(response.data['forms']['similitude']['relevant'])
        self.assertEqual(response.data['forms']['fne']['count'], 3)
        self.assertEqual(response.data['forms']['brouillage']['count'], 2)
        self.assertEqual(response.data['forms']['similitude']['count'], 2)

    def test_eventtypes_list(self):
        '''event types should present the whole list of event types used without duplicates'''
        response = self._get(user=self.qss_user)
        self.assertEqual(
            sorted(response.data['forms']['fne']['event_types']),
            ['ATFM', 'TCAS'])
        response = self._get(user=self.etu_user)
        self.assertEqual(response.data['forms']
                         ['fne']['event_types'], ['ATFM'])

    def test_statuses_list(self):
        '''statuses should present the whole list of statuses used without duplicates'''
        response = self._get(user=self.qss_user)
        self.assertEqual(sorted(response.data['forms']['fne']['statuses']),
                         ['En attente', 'En traitement'])
        self.assertEqual(sorted(response.data['forms']['similitude']['statuses']),
                         ['En attente', 'En traitement'])
        self.assertEqual(
            sorted(response.data['forms']['brouillage']['statuses']),
            ['En attente', 'En traitement'])
        response = self._get(user=self.etu_user)
        self.assertEqual(
            sorted(response.data['forms']['fne']['statuses']), ['En attente'])
        self.assertEqual(
            sorted(response.data['forms']['similitude']['statuses']), [])
        self.assertEqual(
            sorted(response.data['forms']['brouillage']['statuses']),
            ['En attente', 'En traitement'])

    def test_assigned_to(self):
        '''assigned_to should present the whole list of statuses used without duplicates'''
        response = self._get(user=self.qss_user)
        self.assertEqual(sorted(response.data['forms']['fne']['assigned_to']),
                         ['QSS Enquête', 'Sub Etudes'])
        self.assertEqual(
            sorted(response.data['forms']['similitude']['assigned_to']),
            ['QSS Enquête'])
        self.assertEqual(
            sorted(response.data['forms']['brouillage']['assigned_to']),
            ['Sub Etudes'])
        response = self._get(user=self.etu_user)
        self.assertEqual(
            sorted(response.data['forms']['fne']['assigned_to']),
            ['Sub Etudes'])
        self.assertEqual(
            sorted(response.data['forms']['similitude']['assigned_to']), [])
        self.assertEqual(
            sorted(response.data['forms']['brouillage']['assigned_to']),
            ['Sub Etudes'])

    def test_keywords(self):
        '''keywords should present the whole list of statuses used without duplicates'''
        response = self._get(user=self.qss_user)
        self.assertEqual(sorted(response.data['forms']['fne']['keywords']),
                         ['4F', 'Test'])
        self.assertEqual(
            sorted(response.data['forms']['similitude']['keywords']),
            ['4F', 'Test'])
        self.assertEqual(
            sorted(response.data['forms']['brouillage']['keywords']),
            ['4F', 'Test'])
        response = self._get(user=self.etu_user)
        self.assertEqual(
            sorted(response.data['forms']['fne']['keywords']),
            ['4F'])
        self.assertEqual(
            sorted(response.data['forms']['similitude']['keywords']), [])
        self.assertEqual(
            sorted(response.data['forms']['brouillage']['keywords']),
            ['4F', 'Test'])

    def test_warnings_and_alarms(self):
        '''warning and alarms should trigger for old safety events'''
        response = self._get(user=self.qss_user)
        self.assertEqual(response.data['forms']['fne']['warnings'], 1)
        self.assertEqual(response.data['forms']['fne']['alarms'], 1)
        response = self._get(user=self.etu_user)
        self.assertEqual(response.data['forms']['fne']['warnings'], 1)
        self.assertEqual(response.data['forms']['fne']['alarms'], 0)

    def test_zones(self):
        '''zones should present the whole list of team zones without duplicates'''
        response = self._get(user=self.qss_user)
        self.assertEqual(sorted(response.data['forms']['fne']['zones']),
                         ['E', 'W'])
        self.assertEqual(
            sorted(response.data['forms']['similitude']['zones']),
            ['E', 'W'])
        self.assertEqual(
            sorted(response.data['forms']['brouillage']['zones']),
            ['E', 'W'])
        response = self._get(user=self.etu_user)
        self.assertEqual(
            sorted(response.data['forms']['fne']['zones']),
            ['W'])
        self.assertEqual(
            sorted(response.data['forms']['similitude']['zones']), [])
        self.assertEqual(
            sorted(response.data['forms']['brouillage']['zones']),
            ['E', 'W'])
