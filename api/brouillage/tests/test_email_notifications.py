from django.core import mail
from django.contrib.auth.models import Group, Permission

from api.tests.base import *
from shared.models.config import Team
from shared.models.form import Status
from .utils import create_brouillage
from efneproject.celery import notify


class InvestigatorNotificationTest(ApiTestCase):

    def setUp(self):
        super().setUp()
        self.etu_user.email = "etu@apps.crnan"
        self.etu_user.save()
        self.qss_user.email = "qss@apps.crnan"
        self.qss_user.save()
        self.etu_group = Group.objects.get(name="Sub Etudes")
        self.qse_group = Group.objects.get(name="QSS Enquête")
        self.cds_group = Group.objects.get(name="Chef de Salle")
        self.waiting = Status.objects.filter(is_waiting=True).first()
        self.draft = Status.objects.filter(is_draft=True).first()

    def test_brouillage_notification(self):
        '''email should be sent to new brouillage assigned group'''
        self.etu_user.user_permissions.add(Permission.objects.get(
            codename='be_notified_on_brouillage'))
        brouillage = create_brouillage(
            {'status': self.waiting, 'assigned_to_group': self.cds_group})
        brouillage.assigned_to_group = self.etu_group
        brouillage.save()
        brouillage.refresh_from_db()
        self.assertTrue(brouillage.should_notify)
        self.assertEqual(len(mail.outbox), 0)
        notify.delay()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["etu@apps.crnan"])
        self.assertIn("1 nouvelle Fiche Brouillage",
                      mail.outbox[0].subject)
        brouillage.refresh_from_db()
        self.assertFalse(brouillage.should_notify)


class RedactorNotificationTest(ApiTestCase):

    def setUp(self):
        super().setUp()
        self.etu_group = Group.objects.get(name="Sub Etudes")
        self.qse_group = Group.objects.get(name="QSS Enquête")
        self.cds_group = Group.objects.get(name="Chef de Salle")
        self.waiting = Status.objects.filter(is_waiting=True).first()
        self.draft = Status.objects.filter(is_draft=True).first()
        self.progress = Status.objects.filter(is_in_progress=True).first()
        self.done = Status.objects.filter(is_done=True).first()

    def test_brouillage_notification(self):
        '''basic brouillage redactor notification test'''
        # the full workflow is the same as fne which is tested thoroughly
        brouillage = create_brouillage({
            'status': self.done, 'assigned_to_group': self.cds_group,
            'redactors': [{
                'fullname': 'Fullname', 'email': 'redactor3@apps.crnan',
                'team': Team.objects.first()
            }]
        })
        self.assertEqual(len(mail.outbox), 0)
        brouillage.apply_action_by_pk(self.waiting.pk, self.qse_group.pk)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['redactor3@apps.crnan'])
