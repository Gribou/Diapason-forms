from constance import config

from keycloak import KeycloakOpenID
from django.apps import apps


def get_openid_client():
    return KeycloakOpenID(
        server_url=config.KEYCLOAK_SERVER_URL,
        client_id=config.KEYCLOAK_CLIENT_ID,
        realm_name=config.KEYCLOAK_REALM,
        client_secret_key=config.KEYCLOAK_CLIENT_SECRET,
        verify=True)


def has_keycloak_config():
    try:
        return config.KEYCLOAK_ENABLED and apps.get_model(app_label="sso", model_name="SSOConfig").objects.first().well_known_oidc is not None
    except Exception:
        return False


def decode_token(token, sso_config):
    options = {
        "verify_signature": True,
        "verify_aud": False,  # https://github.com/marcospereirampj/python-keycloak/issues/89
        "verify_exp": True
    }
    return get_openid_client().decode_token(
        token, key=sso_config.public_key, options=options)
