from django.contrib.auth.models import Group


from api.tests.base import *
from .utils import create_brouillage
from shared.models.form import Status


class BrouillageFormTest(ApiTestCase):
    url = "/api/brouillage/form/"

    def setUp(self):
        super().setUp()
        self.waiting = Status.objects.filter(is_waiting=True).first()
        self.done = Status.objects.filter(is_done=True).first()
        self.to_be_deleted = Status.objects.filter(
            is_to_be_deleted=True).first()
        self.etu_group = Group.objects.get(name="Sub Etudes")
        self.brouillage = create_brouillage(
            {'status': self.waiting, 'assigned_to_group': self.etu_group})
