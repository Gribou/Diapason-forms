from django.contrib.auth.models import Group
from django.utils import timezone
from constance.test import override_config
from constance import config

from .base import *
from efne.tests.utils import create_fne
from brouillage.tests.utils import create_brouillage
from similitude.tests.utils import create_similitude
from shared.models.config import Team
from shared.models.form import Status
from efne.models import Role
from api.views import CounterViewSet


class CountersTest(ApiTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        waiting = Status.objects.filter(is_waiting=True).first()
        qse_group = Group.objects.get(name="QSS Enquête")
        west_team = Team.objects.filter(zone__short_name="W").first()
        east_team = Team.objects.filter(zone__short_name="E").first()
        other_team = Team.objects.filter(zone__isnull=True).first()
        qss_role = Role.objects.filter(label="QSS").first()
        any_role = Role.objects.exclude(label="QSS").first()
        default_form_data = {'status': waiting, 'assigned_to_group': qse_group,
                             'event_date': timezone.now()}
        create_fne({
            **default_form_data,
            'redactors': [
                {'fullname': 'Fullname', 'role': any_role, 'team': east_team},
                {'fullname': 'Fullname', 'role': any_role, 'team': west_team}
            ]
        })
        create_fne({
            **default_form_data,
            'redactors': [
                {'fullname': 'Fullname', 'role': qss_role, 'team': other_team}
            ]
        })
        create_fne({
            **default_form_data,
            'redactors': [
                {'fullname': 'Fullname', 'role': any_role, 'team': east_team},
            ]
        })
        create_fne({
            **default_form_data,
            'redactors': [
                {'fullname': 'Fullname', 'role': any_role, 'team': other_team},
            ]
        })
        create_similitude({
            **default_form_data,
            'redactors': [
                {'fullname': 'Fullname', 'team': east_team},
                {'fullname': 'Fullname', 'team': west_team},
            ]
        })
        create_similitude({
            **default_form_data,
            'redactors': [
                {'fullname': 'Fullname', 'team': east_team},
            ]
        })
        create_similitude({
            **default_form_data,
            'redactors': [
                {'fullname': 'Fullname', 'team': other_team},
            ]
        })
        create_brouillage({
            **default_form_data,
            'redactors': [
                {'fullname': 'Fullname', 'team': east_team},
                {'fullname': 'Fullname', 'team': west_team},
            ]
        })
        create_brouillage({
            **default_form_data,
            'redactors': [
                {'fullname': 'Fullname', 'team': east_team},
            ]
        })
        create_brouillage({
            **default_form_data,
            'redactors': [
                {'fullname': 'Fullname', 'team': other_team},
            ]
        })

    def _get(self, user=None):
        request = self.factory.get("/api/counters/")
        if user:
            force_authenticate(request, user=user)
        return CounterViewSet.as_view(actions={'get': 'list'})(request)

    @override_config(SHOW_FNE=False)
    def test_show_fne_config(self):
        '''hide fne counters if SHOW_FNE is False'''
        response = self._get()
        self.assertEqual(response.data['forms'], ['similitude', 'brouillage'])
        categories = [d['category']
                      for d in response.data['form_graph']['datasets']]
        self.assertEqual(categories, ['similitude', 'brouillage'])

    @override_config(SHOW_SIMI=False)
    def test_show_fne_config(self):
        '''hide simi counters if SHOW_SIMI is False'''
        response = self._get()
        self.assertEqual(response.data['forms'], ['fne', 'brouillage'])
        categories = [d['category']
                      for d in response.data['form_graph']['datasets']]
        self.assertEqual(categories, ['fne', 'brouillage'])

    @override_config(SHOW_BROUILLAGE=False)
    def test_show_brouillage_config(self):
        '''hide simi counters if SHOW_BROUILLAGE is False'''
        response = self._get()
        self.assertEqual(response.data['forms'], ['fne', 'similitude'])
        categories = [d['category']
                      for d in response.data['form_graph']['datasets']]
        self.assertEqual(categories, ['fne', 'similitude'])

    def test_counters(self):
        response = self._get()
        # Categories
        self.assertEqual([c['name'] for c in response.data['categories']],
                         ['Autres', 'E', 'QSS', 'W'])
        # Totals
        self.assertEqual(response.data['totals']['all'], 10)
        self.assertEqual(response.data['totals']['fne'], 4)
        self.assertEqual(response.data['totals']['similitude'], 3)
        self.assertEqual(response.data['totals']['brouillage'], 3)
        self.assertEqual(response.data['totals']['QSS'], 1)
        self.assertEqual(response.data['totals']['Autres'], 3)
        self.assertEqual(response.data['totals']['E'], 6)
        self.assertEqual(response.data['totals']['W'], 3)
        # Category graph
        category_graph = response.data['category_graph']['datasets']
        self.assertEqual([len(c['data'])
                         for c in category_graph], [6, 6, 6, 6])
        last_month_counts = {c['category']: c['data'][-1]
                             for c in category_graph}
        self.assertEqual(last_month_counts['Autres']['y'], 3)
        self.assertEqual(last_month_counts['E']['y'], 6)
        self.assertEqual(last_month_counts['W']['y'], 3)
        self.assertEqual(last_month_counts['QSS']['y'], 1)
        other_months_counts = [
            any([d['y'] for d in c['data'][:-1]]) for c in category_graph]
        self.assertFalse(any(other_months_counts))
        # Month graph
        month_graph = response.data['form_graph']['datasets']
        self.assertEqual([len(c['data'])
                         for c in month_graph], [6, 6, 6])
        last_month_counts = {c['category']: c['data'][-1]
                             for c in month_graph}
        self.assertEqual(last_month_counts['fne']['y'], 4)
        self.assertEqual(last_month_counts['similitude']['y'], 3)
        self.assertEqual(last_month_counts['brouillage']['y'], 3)
        other_months_counts = [
            any([d['y'] for d in c['data'][:-1]]) for c in month_graph]
        self.assertFalse(any(other_months_counts))
