from api.tests.base import *
from .utils import create_similitude

from shared.models.form import Status
from similitude.models import SimiAction


class GraphTest(ApiTestCase):

    def test_simi_actions_update_on_graph_change(self):
        '''change of Simi graph should trigger rerun_action_graph signal'''
        simi = create_similitude({})
        self.assertEqual(simi.available_actions.count(), 1)
        action = SimiAction.objects.create(
            current_status=simi.status, current_group=simi.assigned_to_group,
            next_status=Status.objects.filter(is_in_progress=True).first())
        simi.refresh_from_db()
        self.assertEqual(simi.available_actions.count(), 2)
        self.assertIn(action, simi.available_actions.all())
