from django.core import mail
from django.contrib.auth.models import Group, Permission

from api.tests.base import *
from shared.models.config import Team
from shared.models.form import Status
from similitude.tests.utils import create_similitude
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

    def test_simi_notification(self):
        '''email should be sent to new simi assigned group'''
        self.qss_user.user_permissions.add(Permission.objects.get(
            codename='be_notified_on_simi'))
        simi = create_similitude(
            {'status': self.waiting, 'assigned_to_group': self.cds_group})
        simi.assigned_to_group = self.qse_group
        simi.save()
        simi.refresh_from_db()
        self.assertTrue(simi.should_notify)
        self.assertEqual(len(mail.outbox), 0)
        notify.delay()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["qss@apps.crnan"])
        self.assertIn("1 nouvelle Fiche Similitude d'Indicatifs",
                      mail.outbox[0].subject)
        simi.refresh_from_db()
        self.assertFalse(simi.should_notify)


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

    def test_simi_notification(self):
        '''basic similitude redactor notification test'''
        # the full workflow is the same as fne which is tested thoroughly
        simi = create_similitude({
            'status': self.done, 'assigned_to_group': self.cds_group,
            'redactors': [{
                'fullname': 'Fullname', 'email': 'redactor2@apps.crnan',
                'team': Team.objects.first()
            }]
        })
        self.assertEqual(len(mail.outbox), 0)
        simi.apply_action_by_pk(self.waiting.pk, self.qse_group.pk)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['redactor2@apps.crnan'])
