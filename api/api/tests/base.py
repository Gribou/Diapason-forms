from django.test import TestCase, override_settings
from rest_framework.test import APIRequestFactory
from django.contrib.auth import get_user_model
from rest_framework.test import force_authenticate
import shutil

import logging
from shared.populate import populate as populate_shared
from efne.populate import populate as populate_efne
from brouillage.populate import populate as populate_brouillage
from similitude.populate import populate as populate_similitude

MEDIA_ROOT_TEST = "fne_test"


@override_settings(MEDIA_ROOT=(MEDIA_ROOT_TEST + "/media"))
class ApiTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        populate_shared.populate_demo(verbose=False)
        populate_efne.populate_demo(verbose=False)
        populate_brouillage.populate_demo(verbose=False)
        populate_similitude.populate_demo(verbose=False)

    def setUp(self):
        logging.disable(logging.ERROR)
        self.factory = APIRequestFactory()
        self.normal_user = get_user_model().objects.create_user(
            username="normal_user", password="normal_user")
        self.cds_user = get_user_model().objects.filter(
            groups__permissions__codename='validator').first()
        self.qss_user = get_user_model().objects.filter(
            groups__permissions__codename='all_access').first()
        self.etu_user = get_user_model().objects.filter(
            groups__name='Sub Etudes').first()

    def tearDown(self):
        logging.disable(logging.NOTSET)
        # manually delete objects so that media are deleted from disk
        try:
            shutil.rmtree(MEDIA_ROOT_TEST)
        except OSError:
            pass

    def _list_view(self, view):
        return view.as_view(actions={'get': 'list', 'post': 'create'})

    def _detail_view(self, view):
        return view.as_view(actions={
            'get': 'retrieve',
            'put': 'update',
            'delete': 'destroy'
        })

    def _get_detail(self, url, user=None, **kwargs):
        request = self.factory.get(url)
        force_authenticate(request, user=user)
        return self._detail_view(self.view)(request, **kwargs)

    def _get_list(self, url, user=None, **kwargs):
        request = self.factory.get(url)
        force_authenticate(request, user=user)
        return self._list_view(self.view)(request, **kwargs)
