from api.tests.base import *
from .utils import create_fne

from shared.models.form import Status
from efne.models import FneAction


class GraphTest(ApiTestCase):

    def test_fne_actions_update_on_graph_change(self):
        '''change of Fne graph should trigger rerun_action_graph signal'''
        fne = create_fne({})
        self.assertEqual(fne.available_actions.count(), 1)
        action = FneAction.objects.create(
            current_status=fne.status, current_group=fne.assigned_to_group,
            next_status=Status.objects.filter(is_in_progress=True).first())
        fne.refresh_from_db()
        self.assertEqual(fne.available_actions.count(), 2)
        self.assertIn(action, fne.available_actions.all())
