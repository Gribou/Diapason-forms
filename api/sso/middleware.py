from django.utils.deprecation import MiddlewareMixin
from django.contrib import messages
from django.contrib.auth import logout
from constance import config


class KeycloakMiddleware(MiddlewareMixin):

    def _user_has_sso(self, request):
        try:
            return request.user.sso_profile is not None
        except:
            return False

    def process_request(self, request):
        if config.KEYCLOAK_ENABLED and self._user_has_sso(request):
            try:
                # if user is logged with SSO (refresh token is present), refresh current user access token or logout user if refresh token has expired
                if request.user.sso_profile.refresh_token is not None:
                    request.user.sso_profile.refresh_access_token()
            except Exception as e:
                # token refresh has failed : force user logout
                try:
                    request.user.sso_profile.logout()
                except:
                    pass
                logout(request)
                messages.add_message(
                    request=request,
                    message="Session terminée",
                    level=messages.WARNING
                )
