from rest_framework import status
from rest_framework.test import force_authenticate
from django.contrib.sessions.middleware import SessionMiddleware

from api.tests.base import *
from sso.views import StandAloneLoginView, LogoutView, SessionView


class StandaloneAuthTest(ApiTestCase):

    def _session_authenticate(self, request):
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

    def test_login_success(self):
        request = self.factory.post("/api/account/token/login/", {
            'username': self.cds_user.username,
            'password': self.cds_user.username
        })
        self._session_authenticate(request)
        response = StandAloneLoginView.as_view()(request)
        self.assertTrue(status.is_success(response.status_code))

    def test_login_failure(self):
        request = self.factory.post("/api/account/token/login/", {
            'username': self.cds_user.username,
            'password': 'wrong password'
        })
        self._session_authenticate(request)
        response = StandAloneLoginView.as_view()(request)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_login_empty(self):
        request = self.factory.post("/api/account/token/login/",
                                    {'username': self.cds_user.username})
        self._session_authenticate(request)
        response = StandAloneLoginView.as_view()(request)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_logout(self):
        request = self.factory.post("/api/account/token/logout/")
        self._session_authenticate(request)
        response = LogoutView.as_view()(request)
        self.assertTrue(status.is_success(response.status_code))

    def test_authenticated_session(self):
        request = self.factory.get("/api/account/session/")
        force_authenticate(request, user=self.cds_user)
        response = SessionView.as_view()(request)
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue(response.data['is_authenticated'])

    def test_anonymous_session(self):
        request = self.factory.get("/api/account/session/")
        response = SessionView.as_view()(request)
        self.assertTrue(status.is_success(response.status_code))
        self.assertFalse(response.data['is_authenticated'])
