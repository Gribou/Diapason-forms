from django.views.generic.base import RedirectView
from django.urls import reverse
from django.http.response import HttpResponseServerError, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from django.shortcuts import resolve_url
import logging

from ..keycloak import get_openid_client, has_keycloak_config

logger = logging.getLogger("django")


class AdminLoginView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        if not has_keycloak_config():
            messages.add_message(
                request=self.request,
                message="L'authentification Keycloak est désactivée (voir Paramètres > Config)",
                level=messages.WARNING
            )
            return reverse("admin:login")
        try:
            redirect_uri = self.request.build_absolute_uri(
                location=reverse('sso:login-complete'))
            self.request.session['redirect_uri'] = redirect_uri
            self.request.session['next_path'] = self.request.build_absolute_uri(
                location=self.request.GET.get('next', reverse("admin:index")))
            return get_openid_client().auth_url(redirect_uri)
        except Exception as e:
            messages.add_message(
                request=self.request,
                message="Echec de la connexion au serveur d'authentification ({})".format(
                    e),
                level=messages.ERROR
            )
            return reverse("admin:login")


class AdminLoginCompleteView(RedirectView):

    def get(self, *args, **kwargs):
        request = self.request
        if 'error' in request.GET:
            return HttpResponseServerError(request.GET['error'])

        if 'code' not in request.GET and 'session_state' not in request.GET:
            return self.response_on_error("réponse incomplète")
        # FIXME should check session_state value but against what ??

        next_path = request.session['next_path']
        redirect_uri = request.session['redirect_uri']
        try:
            user = authenticate(request=request,
                                code=request.GET['code'],
                                redirect_uri=redirect_uri)
            login(request, user,
                  backend='sso.authentication.KeycloakAuthorizationBackend')
            return HttpResponseRedirect(next_path or reverse("admin:index"))
        except Exception as e:
            logger.error(e)
            return self.response_on_error(e)

    def response_on_error(self, error):
        messages.add_message(
            request=self.request,
            message="Echec de la connexion au serveur d'authentification ({})".format(
                error),
            level=messages.ERROR
        )
        return HttpResponseRedirect(reverse("admin:login"))


class AdminLogoutView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        try:
            self.request.user.sso_profile.logout()
        except:
            pass
        logout(self.request)
        if settings.LOGOUT_REDIRECT_URL:
            return resolve_url(settings.LOGOUT_REDIRECT_URL)
        else:
            return reverse('admin:login')
