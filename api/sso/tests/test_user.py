from rest_framework import status
from rest_framework.test import force_authenticate
from djoser.views import UserViewSet

from api.tests.base import *


class UserTest(ApiTestCase):

    def test_get_user(self):
        ''' read user info with user API endpoint'''
        request = self.factory.get("/api/profile/me/")
        force_authenticate(request, user=self.cds_user)
        response = UserViewSet.as_view(actions={'get': 'me'})(request)
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue('shared.validator' in response.data['permissions'])
        self.assertFalse(
            'shared.all_access' in response.data['permissions'])
        self.assertFalse(
            'shared.investigator' in response.data['permissions'])

    def test_form_relevance(self):
        '''relevant form list depends on user groups'''
        request = self.factory.get("/api/profile/me")
        force_authenticate(request, user=self.normal_user)
        response = UserViewSet.as_view(actions={'get': 'me'})(request)
        self.assertFalse(response.data['form_relevance']['brouillage'])
        self.assertFalse(response.data['form_relevance']['fne'])
        self.assertFalse(response.data['form_relevance']['similitude'])
        force_authenticate(request, user=self.etu_user)
        response = UserViewSet.as_view(actions={'get': 'me'})(request)
        self.assertTrue(response.data['form_relevance']['brouillage'])
        self.assertTrue(response.data['form_relevance']['fne'])
        self.assertFalse(response.data['form_relevance']['similitude'])
        force_authenticate(request, user=self.qss_user)
        response = UserViewSet.as_view(actions={'get': 'me'})(request)
        self.assertFalse(response.data['form_relevance']['brouillage'])
        self.assertTrue(response.data['form_relevance']['fne'])
        self.assertTrue(response.data['form_relevance']['similitude'])
