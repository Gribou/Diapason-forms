from rest_framework import status
from django.contrib.auth.models import Group
import lorem

from api.tests.base import *
from .utils import create_brouillage
from shared.models.form import Status
from brouillage.models import PostIt, SubData
from brouillage.views import BrouillageViewSet, PostItViewSet


class BrouillagePostitTest(ApiTestCase):
    url = "/api/brouillage/postit/"
    form_url = "/api/brouillage/form/{}/add_postit/"

    def setUp(self):
        super().setUp()
        waiting = Status.objects.filter(is_waiting=True).first()
        etu_group = Group.objects.get(name="Sub Etudes")
        self.brouillage = create_brouillage(
            {'status': waiting, 'assigned_to_group': etu_group, 'aircrafts': []})

    def test_postit_list_is_not_reachable(self):
        '''endpoint should not answer to list requests'''
        SubData.objects.create(parent=self.brouillage)
        PostIt.objects.create(
            parent=self.brouillage.sub_data, content=lorem.text(), author=self.etu_user)
        PostIt.objects.create(
            parent=self.brouillage.sub_data, content=lorem.text(), author=self.etu_user)
        request = self.factory.get(self.url)
        force_authenticate(request, self.etu_user)
        response = PostItViewSet.as_view(actions={'get': 'list'})(request)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_add_postit_with_author(self):
        '''endpoint should set author according to authenticated user'''
        request = self.factory.post(
            self.form_url.format(self.brouillage.uuid), {'content': lorem.text()}, format="multipart")
        force_authenticate(request, self.etu_user)
        BrouillageViewSet.as_view(
            actions={"post": "add_postit"}, detail=True)(request, uuid=self.brouillage.uuid)
        self.brouillage.refresh_from_db()
        self.assertEqual(
            self.brouillage.sub_data.postits.first().author, self.etu_user)

    def test_postit_update_if_owner(self):
        '''endpoint should update postit only if user is owner'''
        SubData.objects.create(parent=self.brouillage)
        p = PostIt.objects.create(
            parent=self.brouillage.sub_data, content=lorem.text(), author=self.etu_user)
        request = self.factory.put(
            "{}{}/".format(self.url, p.pk), {"content": "Nouveau contenu"})
        force_authenticate(request, self.qss_user)
        response = PostItViewSet.as_view(
            actions={"put": "update"}, detail=True)(request, pk=p.pk)
        self.assertTrue(status.is_client_error(response.status_code))
        self.assertIsNot(
            self.brouillage.sub_data.postits.first().content, "Nouveau contenu")
        force_authenticate(request, self.etu_user)
        response = PostItViewSet.as_view(
            actions={"put": "update"}, detail=True)(request, pk=p.pk)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(
            self.brouillage.sub_data.postits.first().content, "Nouveau contenu")
