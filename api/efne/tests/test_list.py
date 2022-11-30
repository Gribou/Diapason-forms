from django.contrib.auth.models import Group
from django.utils import timezone
from datetime import timedelta


from api.tests.base import *
from .utils import create_fne
from shared.models.form import Status, Team
from efne.models import Role
from efne.views import FneViewSet


class FneFormTest(ApiTestCase):
    url = "/api/fne/form/"

    def setUp(self):
        super().setUp()
        self.waiting = Status.objects.filter(is_waiting=True).first()
        self.qse_group = Group.objects.get(name="QSS Enquête")

    def test_only_show_validated_forms(self):
        '''endpoint should not return non validated forms for all access'''
        cds_group = Group.objects.get(name="Chef de Salle")
        fne1 = create_fne(
            {'status': self.waiting, 'assigned_to_group': cds_group})
        fne2 = create_fne(
            {'status': self.waiting, 'assigned_to_group': self.qse_group})
        request = self.factory.get(self.url)
        force_authenticate(request, self.qss_user)
        response = FneViewSet.as_view(actions={"get": "list"})(request)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results']
                         [0]['uuid'], str(fne2.uuid))

    def test_only_show_assigned_forms(self):
        '''endpoint should return assigned for validators/investigators'''
        cds_group = Group.objects.get(name="Chef de Salle")
        fne1 = create_fne(
            {'status': self.waiting, 'assigned_to_group': cds_group})
        fne2 = create_fne(
            {'status': self.waiting, 'assigned_to_group': self.qse_group})
        request = self.factory.get(self.url)
        force_authenticate(request, self.cds_user)
        response = FneViewSet.as_view(actions={"get": "list"})(request)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results']
                         [0]['uuid'], str(fne1.uuid))

    def test_previous_next_uuid_in_forms(self):
        '''serialized forms should provide previous and next forms uuid'''
        uuid1 = create_fne({
            "event_date": timezone.now(), 'status': self.waiting, 'assigned_to_group': self.qse_group}).uuid
        uuid2 = create_fne({
            "event_date": timezone.now(), 'status': self.waiting, 'assigned_to_group': self.qse_group}).uuid
        request = self.factory.get(self.url)
        force_authenticate(request, self.qss_user)
        response = FneViewSet.as_view(actions={"get": "list"})(request)
        fne1 = response.data['results'][0]
        fne2 = response.data['results'][1]
        self.assertIsNone(fne1['previous_form'])
        self.assertEqual(fne1['next_form'], uuid1)
        self.assertEqual(fne2['previous_form'], uuid2)
        self.assertIsNone(fne2['next_form'])

    def test_sort_by_ref(self):
        """endpoint should handle sort query params"""
        uuid1 = create_fne({
            "event_date": timezone.now(),
            "safetycube": {'reference': "B"}, 'status': self.waiting, 'assigned_to_group': self.qse_group}).uuid
        uuid2 = create_fne({
            "event_date": timezone.now(),  "safetycube": {'reference': "A"}, 'status': self.waiting, 'assigned_to_group': self.qse_group}).uuid
        uuid3 = create_fne({
            "event_date": timezone.now(), 'status': self.waiting, 'assigned_to_group': self.qse_group}).uuid
        request = self.factory.get(self.url)
        force_authenticate(request, self.qss_user)
        response = FneViewSet.as_view(actions={"get": "list"})(request)
        fne1 = response.data['results'][0]
        fne2 = response.data['results'][1]
        fne3 = response.data['results'][2]
        self.assertEqual(fne1['uuid'], str(uuid3))
        self.assertEqual(fne2['uuid'], str(uuid1))
        self.assertEqual(fne3['uuid'], str(uuid2))
        # reverse
        request = self.factory.get(self.url, {'sort': 'ref'})
        force_authenticate(request, self.qss_user)
        response = FneViewSet.as_view(actions={"get": "list"})(request)
        fne1 = response.data['results'][0]
        fne2 = response.data['results'][1]
        fne3 = response.data['results'][2]
        self.assertEqual(fne1['uuid'], str(uuid2))
        self.assertEqual(fne2['uuid'], str(uuid1))
        self.assertEqual(fne3['uuid'], str(uuid3))

    def test_sort_by_date(self):
        """endpoint should handle sort query params"""
        uuid1 = create_fne({
            "event_date": timezone.now() - timedelta(days=1), 'status': self.waiting, 'assigned_to_group': self.qse_group}).uuid
        uuid2 = create_fne({
            "event_date": timezone.now(), 'status': self.waiting, 'assigned_to_group': self.qse_group}).uuid
        request = self.factory.get(self.url, {'sort': 'date'})
        force_authenticate(request, self.qss_user)
        response = FneViewSet.as_view(actions={"get": "list"})(request)
        fne1 = response.data['results'][0]
        fne2 = response.data['results'][1]
        self.assertEqual(fne1['uuid'], str(uuid1))
        self.assertEqual(fne2['uuid'], str(uuid2))
        request = self.factory.get(self.url, {'sort': '-date'})
        force_authenticate(request, self.qss_user)
        response = FneViewSet.as_view(actions={"get": "list"})(request)
        fne1 = response.data['results'][0]
        fne2 = response.data['results'][1]
        self.assertEqual(fne1['uuid'], str(uuid2))
        self.assertEqual(fne2['uuid'], str(uuid1))

    def test_filter_keywords(self):
        '''endpoint should handle keywords query params'''
        fne1 = create_fne(
            {'status': self.waiting, 'assigned_to_group': self.qse_group})
        fne2 = create_fne({'status': self.waiting, 'assigned_to_group': self.qse_group,
                           "keywords": "4F TEST"})
        request = self.factory.get(self.url, {'keywords': '4F'})
        force_authenticate(request, self.qss_user)
        response = FneViewSet.as_view(actions={"get": "list"})(request)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results']
                         [0]['uuid'], str(fne2.uuid))

    def test_filter_status(self):
        '''endpoint should handle status query params'''
        fne1 = create_fne(
            {'status': self.waiting, 'assigned_to_group': self.qse_group})
        fne2 = create_fne({'status': Status.objects.filter(
            is_done=True).first(), 'assigned_to_group': self.qse_group})
        request = self.factory.get(self.url, {'status': self.waiting.label})
        force_authenticate(request, self.qss_user)
        response = FneViewSet.as_view(actions={"get": "list"})(request)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results']
                         [0]['uuid'], str(fne1.uuid))

    def test_filter_group(self):
        '''endpoint should handle group query params'''
        etu_group = Group.objects.get(name="Sub Etudes")
        fne1 = create_fne({
            "event_date": timezone.now(), 'status': self.waiting, 'assigned_to_group': etu_group})
        fne2 = create_fne({
            "event_date": timezone.now(), 'status': self.waiting, 'assigned_to_group': self.qse_group})
        request = self.factory.get(self.url, {'group': etu_group.name})
        force_authenticate(request, self.qss_user)
        response = FneViewSet.as_view(actions={"get": "list"})(request)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results']
                         [0]['uuid'], str(fne1.uuid))

    def test_filter_zone(self):
        '''endpoint should handle zone query params'''
        fne1 = create_fne({
            'status': self.waiting, 'assigned_to_group': self.qse_group,
            'redactors': [{
                'fullname': 'Fullname', 'team': Team.objects.filter(zone__short_name="E").first(),
                'role': Role.objects.first()}]
        })
        fne2 = create_fne({
            'status': self.waiting, 'assigned_to_group': self.qse_group, 'redactors': [{
                'fullname': 'Fullname', 'team': Team.objects.filter(zone__short_name="W").first(),
                'role': Role.objects.first()}]})
        request = self.factory.get(self.url, {'zone': "W"})
        force_authenticate(request, self.qss_user)
        response = FneViewSet.as_view(actions={"get": "list"})(request)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results']
                         [0]['uuid'], str(fne2.uuid))
