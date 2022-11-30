from rest_framework import status

from .base import *
from api.views import ConfigViewSet, HealthCheckView
from shared.tasks import check_graph


class DemoConfigTest(ApiTestCase):

    def test_read_config(self):
        request = self.factory.get("/api/config/")
        response = ConfigViewSet.as_view(actions={'get': 'list'})(request)
        self.assertTrue(status.is_success(response.status_code))
        self.assertIsNotNone(response.data['shared'])
        self.assertIsNotNone(response.data['fne'])
        self.assertIsNotNone(response.data['fne']['event_types'])
        self.assertIsNotNone(response.data['fne']['tech_event_types'])
        self.assertIsNotNone(response.data['fne']['roles'])
        self.assertIsNotNone(response.data['brouillage'])
        self.assertIsNotNone(response.data['brouillage']['interference_types'])
        self.assertIsNotNone(response.data['shared']['teams'])
        self.assertIsNotNone(response.data['shared']['groups'])
        self.assertIsNotNone(response.data['shared']['sectors'])
        self.assertIsNotNone(response.data['shared']['positions'])
        self.assertIsNotNone(response.data['shared']['sector_groups'])
        self.assertIsNotNone(response.data['shared']['custom_forms'])
        self.assertIsNotNone(response.data['shared']['features'])
        self.assertTrue(response.data['shared']['features']['has_zones'])

    def test_check_fne_graph(self):
        ''' check that demo graph is complete and do not raise errors'''
        self.assertFalse("INCOMPLET" in check_graph.delay(
            app_label='similitude', action_model_name='Simi').get())
        self.assertFalse("INCOMPLET" in check_graph.delay(
            app_label='efne', action_model_name='Fne').get())
        self.assertFalse("INCOMPLET" in check_graph.delay(
            app_label='brouillage', action_model_name='Brouillage').get())


class HealthCheckTest(ApiTestCase):

    def test_healthcheck(self):
        request = self.factory.get("/api/health/")
        response = HealthCheckView.as_view()(request)
        self.assertTrue(status.is_success(response.status_code))
