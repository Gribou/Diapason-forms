from rest_framework import status
from django.contrib.auth.models import Group
import lorem

from api.tests.base import *
from .utils import create_similitude
from shared.models.form import Status
from similitude.models import PostIt
from similitude.views import SimiViewSet, PostItViewSet


class SimiPostitTest(ApiTestCase):
    url = "/api/similitude/postit/"
    form_url = "/api/similitude/form/{}/add_postit/"

    def setUp(self):
        super().setUp()
        waiting = Status.objects.filter(is_waiting=True).first()
        etu_group = Group.objects.get(name="Sub Etudes")
        self.simi = create_similitude(
            {'status': waiting, 'assigned_to_group': etu_group, 'aircrafts': [], 'sub_data': {'inca_number': "1234"}})

    def test_postit_list_is_not_reachable(self):
        '''endpoint should not answer to list requests'''
        PostIt.objects.create(
            parent=self.simi.sub_data, content=lorem.text(), author=self.qss_user)
        PostIt.objects.create(
            parent=self.simi.sub_data, content=lorem.text(), author=self.etu_user)
        request = self.factory.get(self.url)
        force_authenticate(request, self.qss_user)
        response = PostItViewSet.as_view(actions={'get': 'list'})(request)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_add_postit_with_author(self):
        '''endpoint should set author according to authenticated user'''
        request = self.factory.post(
            self.form_url.format(self.simi.uuid), {'content': lorem.text()}, format="multipart")
        force_authenticate(request, self.qss_user)
        SimiViewSet.as_view(
            actions={"post": "add_postit"}, detail=True)(request, uuid=self.simi.uuid)
        self.simi.refresh_from_db()
        self.assertEqual(
            self.simi.sub_data.postits.first().author, self.qss_user)
        force_authenticate(request, self.etu_user)
        SimiViewSet.as_view(
            actions={"post": "add_postit"}, detail=True)(request, uuid=self.simi.uuid)
        self.simi.refresh_from_db()
        self.assertEqual(self.simi.sub_data.postits.count(), 2)
        self.assertEqual(
            self.simi.sub_data.postits.last().author, self.etu_user)

    def test_postit_update_if_owner(self):
        '''endpoint should update postit only if user is owner'''
        p = PostIt.objects.create(
            parent=self.simi.sub_data, content=lorem.text(), author=self.etu_user)
        request = self.factory.put(
            "{}{}/".format(self.url, p.pk), {"content": "Nouveau contenu"})
        force_authenticate(request, self.qss_user)
        response = PostItViewSet.as_view(
            actions={"put": "update"}, detail=True)(request, pk=p.pk)
        self.assertTrue(status.is_client_error(response.status_code))
        self.assertIsNot(
            self.simi.sub_data.postits.first().content, "Nouveau contenu")
        force_authenticate(request, self.etu_user)
        response = PostItViewSet.as_view(
            actions={"put": "update"}, detail=True)(request, pk=p.pk)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(
            self.simi.sub_data.postits.first().content, "Nouveau contenu")
