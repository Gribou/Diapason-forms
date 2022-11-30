from api.tests.base import *
from .utils import create_brouillage

from shared.models.form import Status
from brouillage.models import BrouillageAction


class GraphTest(ApiTestCase):

    def test_brouillage_actions_update_on_graph_change(self):
        '''change of Brouillage graph should trigger rerun_action_graph signal'''
        brouillage = create_brouillage({})
        self.assertEqual(brouillage.available_actions.count(), 1)
        action = BrouillageAction.objects.create(
            current_status=brouillage.status, current_group=brouillage.assigned_to_group,
            next_status=Status.objects.filter(is_in_progress=True).first())
        brouillage.refresh_from_db()
        self.assertEqual(brouillage.available_actions.count(), 2)
        self.assertIn(action, brouillage.available_actions.all())
