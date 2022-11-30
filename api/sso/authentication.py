
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.db import transaction
from django.utils import timezone
from rest_framework.authentication import SessionAuthentication

from .keycloak import decode_token, get_openid_client, has_keycloak_config
from .models import SSOUserProfile, get_sso_config


class CSRFExemptSessionAuthentication(SessionAuthentication):
    '''Disable Csrf checks entirely when authenticating through API
    X-CSRF-Token is overwritten by Traefik and ADAN portal so check cannot be done properly
    ATM2 Reverse proxy enforces its own checks so attack surface stays fairly limited.
    '''

    def enforce_csrf(self, request):
        return

# OpenID Connect Flow :
# https://www.pingidentity.com/fr/resources/client-library/articles/openid-connect.html


def _get_username_from_token(id_token):
    username = id_token.get('preferred_username', None)
    if username is None:
        username = id_token.get('email', None)
        if username is not None:
            username = username.split("@")[0]
    if username is None:
        username = id_token.get('sub')
    return username


def _update_or_create_user_from_sso(id_token_object):
    with transaction.atomic():
        user, _ = get_user_model().objects.update_or_create(
            username=_get_username_from_token(id_token_object),
            defaults={
                'email': id_token_object.get('email', '')
            }
        )
        profile, _ = SSOUserProfile.objects.update_or_create(
            sub=id_token_object.get('sub'), defaults={'user': user})
        return profile


class KeycloakAuthorizationBackend(BaseBackend):

    def get_user(self, user_id):
        try:
            user = get_user_model().objects.select_related('sso_profile').get(pk=user_id)
            if user.sso_profile.refresh_expires_before > timezone.now():
                return user
        except Exception:
            pass

    def authenticate(self, request, code, redirect_uri):
        # code is what keycloak returns to user when login is complete
        # it must be exchanged by this backend for tokens
        # redirect_uri must be the same as the one used to get 'code'
        if has_keycloak_config():
            initiate_time = timezone.now()
            tokens = get_openid_client().token(code=code, grant_type=[
                "authorization_code"], redirect_uri=redirect_uri)
            token_key = 'id_token' if 'id_token' in tokens else 'access_token'
            token_object = decode_token(tokens[token_key], get_sso_config())
            profile = _update_or_create_user_from_sso(token_object)
            profile.login(tokens, initiate_time)
            return profile.user
