from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from djoser.conf import settings as djoser_settings
import logging
import json

from shared.serializers.config import get_serialized_notifications
from .keycloak import get_openid_client, has_keycloak_config

logger = logging.getLogger("django")


class SSOLoginView(APIView):
    '''
    Demande d'authentification auprès du serveur SSO (Keycloak)
    Le serveur renvoie une URL d'autorisation Keycloak qui permettra d'obtenir un code à utiliser avec la vue api-sso-callback
    '''
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        if not has_keycloak_config():
            return Response({"non_field_errors": "L'authentification Angélique est désactivée. Veuillez utiliser le formulaire de connexion intégré."}, status=status.HTTP_400_BAD_REQUEST)
        redirect_uri = request.data.get('redirect_uri', "")
        # Returns the url the user needs to go to to authenticate with keycloak
        return Response({"authorization_url": get_openid_client().auth_url(redirect_uri)})


class SSOCallbackView(APIView):
    '''
    Termine le processus d'authentification SSO (Keycloak)
    Indiquez ici les valeurs obtenues auprès du serveur d'authentification sous la forme :
    { "code" : "le-code", "redirect_uri": "uri-fournit-par-sso"}
    '''
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        if not has_keycloak_config():
            return Response({"non_field_errors": "L'authentification Angélique est désactivée. Veuillez utiliser le formulaire de connexion intégré."}, status=status.HTTP_400_BAD_REQUEST)
        code = request.data.get('code', None)
        redirect_uri = request.data.get('redirect_uri', "")
        try:
            user = authenticate(request=request,
                                code=code,
                                redirect_uri=redirect_uri)
            login(request, user,
                  backend='sso.authentication.KeycloakAuthorizationBackend')
            if settings.DEBUG:
                token, _ = djoser_settings.TOKEN_MODEL.objects.get_or_create(
                    user=user)
                return Response(djoser_settings.SERIALIZERS.token(token).data)
            else:
                return Response({'detail': 'Authentifié avec succès.'})
        except Exception as e:
            logger.error(e)
            error_message = json.loads(e.error_message).get(
                "error_description", None)
            return Response(
                {'non_field_errors': "L'authentification Angélique a échoué ({}).".format(
                    error_message or e)},
                status=status.HTTP_400_BAD_REQUEST)


class StandAloneLoginView(APIView):
    """
    Authentification de l'utilisateur. Fournit les cookies 'csrftoken' et 'sessionid' à utiliser pour les requêtes ultérieures
    """
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        # This is not called in DEBUG. Djoser login is used instead
        try:
            username = request.data.get('username', None)
            password = request.data.get('password', None)
        except:
            # request.data may not be a dict...
            pass
        if username is None or password is None:
            return Response(
                {
                    'non_field_errors':
                    'Veuillez indiquer nom d\'utilisateur et mot de passe.'
                },
                status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'non_field_errors': 'Mot de passe invalide.'},
                            status=status.HTTP_400_BAD_REQUEST)

        login(request, user)
        return Response({'detail': 'Authentifié avec succès.'})


class LogoutView(APIView):
    """
    Déconnexion de l'utilisateur :
    Invalidation des cookies de session
    Force la déconnexion auprès du serveur SSO le cas échéant
    """

    def post(self, request, format=None):
        try:
            self.request.user.sso_profile.logout()
        except:
            pass
        if settings.DEBUG:
            djoser_settings.TOKEN_MODEL.objects.filter(
                user=request.user).delete()
        logout(request)
        return Response({'detail': 'Déconnecté avec succès.'})


class SessionView(APIView):
    """
    Récupération des cookies pour la session en cours. Vérification de l'authentification de l'utilisateur courant
    """
    permission_classes = [AllowAny]

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, format=None):
        # FIXME this does not return authenticated just after login callback success
        return Response({'is_authenticated': request.user.is_authenticated})


class UserPermissionUpdate(APIView):
    """
    Permet à l'utilisateur authentifié de personnaliser ses préferences concernant les notifications.
    Body sour la forme : {"notifications": ["shared.be_notified_on_fne", "shared.be_notified_on_simi"]}
    Voir api/shared/models/config.py pour le détail des permissions existantes.
    """
    available_permissions = [n['permission']
                             for n in get_serialized_notifications()]

    def post(self, request, format=None):
        notifications = request.data.get("notifications", {})
        for codename, enabled in notifications.items():
            if codename not in self.available_permissions:
                # only allow permissions from list or user could grant itself more privileges (ex : become all_access)
                return Response({"non_field_errors": "'{}' n'est pas une valeur possible.".format(codename)}, status=status.HTTP_400_BAD_REQUEST)
            perm = Permission.objects.filter(
                codename=codename.split(".")[-1]).first()
            if perm is None:
                return Response({"non_field_errors": "'{}' n'est pas une valeur possible.".format(codename)}, status=status.HTTP_400_BAD_REQUEST)
            if enabled:
                request.user.user_permissions.add(perm)
            else:
                request.user.user_permissions.remove(perm)
        return Response(status=status.HTTP_204_NO_CONTENT)
