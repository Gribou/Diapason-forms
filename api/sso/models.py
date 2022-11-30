from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.utils import timezone
import logging
import json

from .keycloak import get_openid_client

logger = logging.getLogger("django")


class SSOConfig(models.Model):

    _well_known_oidc = models.TextField(blank=True)

    @property
    def well_known_oidc(self):
        return json.loads(self._well_known_oidc)

    @well_known_oidc.setter
    def well_known_oidc(self, content):
        self._well_known_oidc = json.dumps(content)

    def save(self, *args, **kwargs):
        if not self.pk and SSOConfig.objects.exists():
            raise ValidationError(
                'There is can be only one SSOConfig instance')
        return super().save(*args, **kwargs)

    public_key = models.TextField(blank=True)


def get_sso_config():
    return SSOConfig.objects.first()


class SSOUserProfile(models.Model):
    user = models.OneToOneField(get_user_model(),
                                related_name='sso_profile',
                                on_delete=models.CASCADE)
    sub = models.CharField(max_length=255, unique=True)
    access_token = models.TextField(null=True)
    expires_before = models.DateTimeField(null=True)

    refresh_token = models.TextField(null=True)
    refresh_expires_before = models.DateTimeField(null=True)

    def logout(self):
        # Try to logout from keycloak server.
        # if fails, continue anyway
        try:
            get_openid_client().logout(self.refresh_token)
        except:
            pass
        self.access_token = None
        self.expires_before = None
        self.refresh_token = None
        self.refresh_expires_before = None
        self.save()

    def login(self, token_response, initiate_time):
        expires_before = initiate_time + timedelta(
            seconds=token_response['expires_in'])
        refresh_expires_before = initiate_time + timedelta(
            seconds=token_response['refresh_expires_in'])
        self.access_token = token_response['access_token']
        self.expires_before = expires_before
        self.refresh_token = token_response['refresh_token']
        self.refresh_expires_before = refresh_expires_before
        self.save()

    def refresh_access_token(self):
        if self.refresh_expires_before >= timezone.now():
            initiate_time = timezone.now()
            self.login(get_openid_client().refresh_token(self.refresh_token),
                       initiate_time)
        else:
            raise Exception("Refresh token has expired")

    def check_session(self):
        # check that the refresh token is still active = the user has not logout from another app
        return get_openid_client().introspect(self.refresh_token).get('active', False)
