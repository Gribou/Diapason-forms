from constance.test import override_config

from api.tests.base import *
from sso.populate import populate
from sso.models import SSOConfig, get_sso_config
from sso.keycloak import has_keycloak_config
from sso.authentication import _update_or_create_user_from_sso


@override_config(KEYCLOAK_ENABLED=True)
class SSOTest(ApiTestCase):

    def setUp(self):
        super().setUp()
        populate()
        sso = get_sso_config()
        sso.well_known_oidc = {
            'issuer': 'https://keycloak.example.com/auth/realms/test'
        }
        sso.public_key = "-----BEGIN PUBLIC KEY-----\nThisIsAPublicKey\n-----END PUBLIC KEY-----"
        sso.save()

    def test_sso_config(self):
        self.assertTrue(SSOConfig.objects.exists())
        self.assertTrue(has_keycloak_config())

        SSOConfig.objects.all().delete()
        self.assertFalse(has_keycloak_config())

    def test_create_user_from_sso(self):
        '''should create a new user from sso id object'''
        id_object = {
            "email": "prenom.nom@aviation-civile.gouv.fr", "sub": "123456"}
        _update_or_create_user_from_sso(id_object)
        new_user = get_user_model().objects.get(username="prenom.nom")
        self.assertEqual(new_user.email, "prenom.nom@aviation-civile.gouv.fr")
        self.assertEqual(new_user.sso_profile.sub, "123456")

        id_object = {
            "preferred_username": "MyName",
            "email": "my.name@aviation-civile.gouv.fr", "sub": "567890"}
        _update_or_create_user_from_sso(id_object)
        new_user = get_user_model().objects.get(username="MyName")
        self.assertEqual(new_user.email, "my.name@aviation-civile.gouv.fr")
        self.assertEqual(new_user.sso_profile.sub, "567890")
        self.assertFalse(get_user_model().objects.filter(
            username="my.name").exists())

        id_object = {"sub": "abcdef"}
        _update_or_create_user_from_sso(id_object)
        new_user = get_user_model().objects.get(username="abcdef")
        self.assertEqual(new_user.sso_profile.sub, "abcdef")

    def test_update_user_from_sso(self):
        '''should update an existing user from sso id object'''
        existing_user = get_user_model().objects.create_user(
            "prenom.nom", None, "my_password")
        id_object = {
            "email": "prenom.nom@aviation-civile.gouv.fr", "sub": "123456"}
        _update_or_create_user_from_sso(id_object)
        existing_user.refresh_from_db()
        self.assertEqual(existing_user.email,
                         "prenom.nom@aviation-civile.gouv.fr")
        self.assertEqual(existing_user.sso_profile.sub, "123456")

    # FIXME : how to mock KeycloakOpenId client ?
    # TODO refresh sso_config
    # TODO refresh token in keycloak middelware
    # TODO user login and login callback
    # TODO user logout = feycloak logout
