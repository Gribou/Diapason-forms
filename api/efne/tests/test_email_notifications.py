from django.core import mail
from django.contrib.auth.models import Group, Permission

from api.tests.base import *
from shared.models.config import Team
from shared.models.form import Status
from efne.models import Role
from efne.tests.utils import create_fne
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

    def test_fne_notification(self):
        '''email should be sent to new fne assigned group'''
        self.etu_user.user_permissions.add(Permission.objects.get(
            codename='be_notified_on_fne'))
        fne = create_fne(
            {'status': self.waiting, 'assigned_to_group': self.qse_group})
        fne.assigned_to_group = self.etu_group
        fne.save()
        fne.refresh_from_db()
        self.assertTrue(fne.should_notify)
        self.assertEqual(len(mail.outbox), 0)
        notify.delay()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["etu@apps.crnan"])
        self.assertIn("1 nouvelle Fiche de Notification d'Evènement",
                      mail.outbox[0].subject)
        fne.refresh_from_db()
        self.assertFalse(fne.should_notify)


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

    def populate_fne(self, status, group):
        return create_fne({
            'status': status, 'assigned_to_group': group,
            'redactors': [{
                'fullname': 'Fullname', 'email': 'redactor@apps.crnan',
                'team': Team.objects.first(), 'role': Role.objects.first()
            }],
            'safetycube': {'reference': "1234", 'status': "OPEN"}
        })

    def test_fne_notification_on_transfer_to_validator(self):
        '''redactor should not be notified when form is transfered to validator'''
        fne = self.populate_fne(self.draft, None)
        self.assertEqual(len(mail.outbox), 0)
        # transfer to cds for validation
        fne.apply_default_action()
        self.assertEqual(fne.assigned_to_group.pk, self.cds_group.pk)
        self.assertEqual(len(mail.outbox), 0)
        # validator sets as done : no email
        fne.apply_default_action()  # -> done for cds
        self.assertTrue(fne.status.is_done)
        self.assertEqual(len(mail.outbox), 0)

    def test_fne_notification_on_transfer_between_groups(self):
        '''redactor should be notified when form is transferred between groups'''
        fne = self.populate_fne(self.waiting, self.cds_group)
        self.assertEqual(len(mail.outbox), 0)
        # transfer to qss
        fne.apply_action_by_pk(self.waiting.pk, self.qse_group.pk)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['redactor@apps.crnan'])
        # transfer to etu
        fne.apply_action_by_pk(self.waiting.pk, self.etu_group.pk)
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[1].to, ['redactor@apps.crnan'])

    def test_fne_notification_on_status_change(self):
        '''redactor should not be notified when form changes status'''
        fne = self.populate_fne(self.waiting, self.qse_group)
        self.assertEqual(len(mail.outbox), 0)
        # state change (no mail)
        fne.apply_action_by_pk(self.progress.pk, self.qse_group.pk)
        self.assertEqual(len(mail.outbox), 0)

    def test_fne_notification_on_status_done(self):
        '''redactor should be notified when becomes 'done' for investigators'''
        fne = self.populate_fne(self.waiting, self.qse_group)
        self.assertEqual(len(mail.outbox), 0)
        fne.apply_action_by_pk(self.done.pk, self.qse_group.pk)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['redactor@apps.crnan'])
