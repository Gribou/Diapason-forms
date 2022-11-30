from rest_framework import status
from rest_framework.test import RequestsClient

from .base import *


class RouterTest(ApiTestCase):

    def test_root_view(self):
        '''API Root View should list all available endpoints'''
        client = RequestsClient()
        response = client.get("http://testserver/api/")
        self.assertTrue(status.is_success(response.status_code))
        content = response.json()
        self.assertTrue(sorted(content.keys()) == sorted([
                        'profile', 'config', 'counters', 'meta', 'login', 'logout', 'session', 'fne', 'similitude', 'brouillage', 'custom', 'sso-login', 'sso-login-callback', 'health', 'permissions']))
        self.assertTrue(sorted(content['fne']) ==
                        sorted(['form', 'postit', 'attachment', 'draft']))
        self.assertTrue(sorted(content['similitude']) ==
                        sorted(['form', 'postit', 'draft']))
        self.assertTrue(sorted(content['brouillage']) ==
                        sorted(['form', 'postit', 'draft']))
