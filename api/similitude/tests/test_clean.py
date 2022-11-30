from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import Group

from api.tests.base import *
from efneproject.celery import clean
from shared.models.form import Status
from shared.models.config import group_is_investigator, group_is_validator
from ..models import Simi
from .utils import create_similitude


class FormCleaningTest(ApiTestCase):

    def test_obsolete_drafts(self):
        '''obsolete drafts should be deleted'''
        b = create_similitude({
            'event_date': timezone.now() - timedelta(hours=52),
            'status': Status.objects.filter(is_draft=True).first()
        })
        clean.delay()
        self.assertFalse(Simi.objects.filter(uuid=b.uuid).exists())

    def test_non_obsolete_drafts(self):
        '''non obsolete drafts should not be touched'''
        b = create_similitude({
            'event_date': timezone.now() - timedelta(hours=6),
            'status': Status.objects.filter(is_draft=True).first()
        })
        clean.delay()
        b.refresh_from_db()
        self.assertTrue(b.status.is_draft)

    def test_obsolete_waiting_for_validation(self):
        '''form waiting for validation for too long are transfer to investigators'''
        b = create_similitude({
            'event_date': timezone.now() - timedelta(hours=28),
            'status': Status.objects.filter(is_waiting=True).first(),
            'assigned_to_group': Group.objects.filter(name="Chef de Salle").first()
        })
        clean.delay()
        b.refresh_from_db()
        self.assertTrue(b.status.is_waiting)
        self.assertTrue(group_is_investigator(b.assigned_to_group))

    def test_non_obsolete_waiting_for_validation(self):
        '''form waiting for validation not for long enough should not be touched'''
        b = create_similitude({
            'event_date': timezone.now() - timedelta(hours=6),
            'status': Status.objects.filter(is_waiting=True).first(),
            'assigned_to_group': Group.objects.filter(name="Chef de Salle").first()
        })
        clean.delay()
        b.refresh_from_db()
        self.assertTrue(b.status.is_waiting)
        self.assertTrue(group_is_validator(b.assigned_to_group))

    def test_validated(self):
        '''validated forms are transfer to investigators'''
        b = create_similitude({
            'event_date': timezone.now() - timedelta(hours=2),
            'status': Status.objects.filter(is_done=True).first(),
            'assigned_to_group': Group.objects.filter(name="Chef de Salle").first()
        })
        clean.delay()
        b.refresh_from_db()
        self.assertTrue(b.status.is_waiting)
        self.assertTrue(group_is_investigator(b.assigned_to_group))

    def test_marked_for_deletion(self):
        '''forms marked for deletion and existing for more than configured delay are deleted'''
        b = create_similitude({
            'event_date': timezone.now() - timedelta(hours=28),
            'status': Status.objects.filter(is_to_be_deleted=True).first()
        })
        clean.delay()
        self.assertFalse(Simi.objects.filter(uuid=b.uuid).exists())

    def test_recent_marked_for_deletion(self):
        '''too recent forms marked for deletion should not be touched'''
        b = create_similitude({
            'event_date': timezone.now() - timedelta(hours=6),
            'status': Status.objects.filter(is_to_be_deleted=True).first()
        })
        clean.delay()
        b.refresh_from_db()
        self.assertTrue(b.status.is_to_be_deleted)
