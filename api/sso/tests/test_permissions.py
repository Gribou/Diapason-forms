from rest_framework import status
from django.contrib.auth.models import Permission

from api.tests.base import *
from sso.views import UserPermissionUpdate


class UserPermissionTest(ApiTestCase):
    url = "/api/sso/permissions/"

    def setUp(self):
        super().setUp()
        self.fne_notif = Permission.objects.get(codename="be_notified_on_fne")
        self.simi_notif = Permission.objects.get(
            codename="be_notified_on_simi")
        self.brouillage_notif = Permission.objects.get(
            codename="be_notified_on_brouillage")

    def test_add_user_permission(self):
        data = {'notifications': {
            'shared.be_notified_on_fne': True,
            'shared.be_notified_on_simi': True,
            'shared.be_notified_on_brouillage': False
        }}
        request = self.factory.post(self.url, data=data)
        force_authenticate(request, user=self.normal_user)
        response = UserPermissionUpdate.as_view()(request)
        self.assertTrue(status.is_success(response.status_code))
        self.assertIn(self.fne_notif,
                      self.normal_user.user_permissions.all())
        self.assertIn(self.simi_notif,
                      self.normal_user.user_permissions.all())
        self.assertNotIn(self.brouillage_notif,
                         self.normal_user.user_permissions.all())

    def test_remove_user_permission(self):
        self.normal_user.user_permissions.add(self.brouillage_notif)
        data = {'notifications': {
            'shared.be_notified_on_fne': True,
            'shared.be_notified_on_simi': True,
            'shared.be_notified_on_brouillage': False
        }}
        self.assertIn(self.brouillage_notif,
                      self.normal_user.user_permissions.all())
        request = self.factory.post(self.url, data=data)
        force_authenticate(request, user=self.normal_user)
        response = UserPermissionUpdate.as_view()(request)
        self.assertTrue(status.is_success(response.status_code))
        self.assertNotIn(self.brouillage_notif,
                         self.normal_user.user_permissions.all())

    def test_invalid_user_permission(self):
        all_access = Permission.objects.get(codename="all_access")
        data = {'notifications': {
            'shared.all_access': True,
        }}
        request = self.factory.post(self.url, data=data)
        force_authenticate(request, user=self.normal_user)
        response = UserPermissionUpdate.as_view()(request)
        self.assertTrue(status.is_client_error(response.status_code))
        self.assertNotIn(all_access,
                         self.normal_user.user_permissions.all())

        data = {'notifications': {
            'shared.not_a_permission': True,
        }}
        request = self.factory.post(self.url, data=data)
        force_authenticate(request, user=self.normal_user)
        response = UserPermissionUpdate.as_view()(request)
        self.assertTrue(status.is_client_error(response.status_code))
