from rest_framework import status
from django.contrib.auth.models import Group
import lorem

from api.tests.base import *
from .utils import create_fne
from shared.models.form import Status
from efne.models import PostIt, SubData
from efne.views import FneViewSet, PostItViewSet


class FnePostitTest(ApiTestCase):
    url = "/api/fne/postit/"
    form_url = "/api/fne/form/{}/add_postit/"

    def setUp(self):
        super().setUp()
        waiting = Status.objects.filter(is_waiting=True).first()
        etu_group = Group.objects.get(name="Sub Etudes")
        self.fne = create_fne(
            {'status': waiting, 'assigned_to_group': etu_group, 'aircrafts': []})
        SubData.objects.create(parent_fne=self.fne)
        self.fne.refresh_from_db()

    def test_add_postit_if_assigned(self):
        '''postit creation should fail if form is not attributed to user'''
        qse_group = Group.objects.get(name="QSS Enquête")
        self.fne.assigned_to_group = qse_group
        self.fne.save()
        request = self.factory.post(
            self.form_url.format(self.fne.uuid), {'content': lorem.text()}, format="multipart")
        force_authenticate(request, self.etu_user)
        response = FneViewSet.as_view(
            actions={"post": "add_postit"}, detail=True)(request, uuid=self.fne.uuid)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_add_postit_if_all_access(self):
        '''postit should be created if user is all access'''
        request = self.factory.post(
            self.form_url.format(self.fne.uuid), {'content': lorem.text()}, format="multipart")
        force_authenticate(request, self.qss_user)
        response = FneViewSet.as_view(
            actions={"post": "add_postit"}, detail=True)(request, uuid=self.fne.uuid)
        self.assertTrue(status.is_success(response.status_code))
        self.fne.refresh_from_db()
        self.assertEqual(self.fne.sub_data.postits.count(), 1)

    def test_add_postit_with_author(self):
        '''endpoint should set author according to authenticated user'''
        request = self.factory.post(
            self.form_url.format(self.fne.uuid), {'content': lorem.text()}, format="multipart")
        force_authenticate(request, self.qss_user)
        FneViewSet.as_view(
            actions={"post": "add_postit"}, detail=True)(request, uuid=self.fne.uuid)
        self.fne.refresh_from_db()
        self.assertEqual(
            self.fne.sub_data.postits.first().author, self.qss_user)
        force_authenticate(request, self.etu_user)
        FneViewSet.as_view(
            actions={"post": "add_postit"}, detail=True)(request, uuid=self.fne.uuid)
        self.fne.refresh_from_db()
        self.assertEqual(self.fne.sub_data.postits.count(), 2)
        self.assertEqual(
            self.fne.sub_data.postits.last().author, self.etu_user)

    def test_postit_list_is_not_reachable(self):
        '''endpoint should not answer to list requests'''
        PostIt.objects.create(
            parent=self.fne.sub_data, content=lorem.text(), author=self.qss_user)
        PostIt.objects.create(
            parent=self.fne.sub_data, content=lorem.text(), author=self.etu_user)
        request = self.factory.get(self.url)
        force_authenticate(request, self.qss_user)
        response = PostItViewSet.as_view(actions={'get': 'list'})(request)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_postit_update_if_owner(self):
        '''endpoint should update postit only if user is owner'''
        p = PostIt.objects.create(
            parent=self.fne.sub_data, content=lorem.text(), author=self.etu_user)
        request = self.factory.put(
            "{}{}/".format(self.url, p.pk), {"content": "Nouveau contenu"})
        force_authenticate(request, self.qss_user)
        response = PostItViewSet.as_view(
            actions={"put": "update"}, detail=True)(request, pk=p.pk)
        self.assertTrue(status.is_client_error(response.status_code))
        self.assertIsNot(
            self.fne.sub_data.postits.first().content, "Nouveau contenu")
        force_authenticate(request, self.etu_user)
        response = PostItViewSet.as_view(
            actions={"put": "update"}, detail=True)(request, pk=p.pk)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(
            self.fne.sub_data.postits.first().content, "Nouveau contenu")

    def test_postit_delete_if_owner(self):
        '''endpoints should destroy postit only if user is owner'''
        p = PostIt.objects.create(
            parent=self.fne.sub_data, content=lorem.text(), author=self.etu_user)
        request = self.factory.delete("{}{}/".format(self.url, p.pk))
        force_authenticate(request, self.qss_user)
        response = PostItViewSet.as_view(
            actions={"delete": "destroy"}, detail=True)(request, pk=p.pk)
        self.assertTrue(status.is_client_error(response.status_code))
        self.assertEqual(self.fne.sub_data.postits.count(), 1)
        force_authenticate(request, self.etu_user)
        response = PostItViewSet.as_view(
            actions={"delete": "destroy"}, detail=True)(request, pk=p.pk)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(self.fne.sub_data.postits.count(), 0)
