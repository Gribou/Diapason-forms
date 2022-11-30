from django.urls import path
from django.conf import settings
from djoser.views import TokenCreateView

from .views import SSOLoginView, SSOCallbackView, StandAloneLoginView, LogoutView, SessionView, UserPermissionUpdate

urlpatterns = [
    path('sso/login/', SSOLoginView.as_view(), name="api-sso-login"),
    path('sso/login/callback/', SSOCallbackView.as_view(),
         name="api-sso-login-complete"),
    path('profile/me/permissions/',
         UserPermissionUpdate.as_view(), name="api-permissions"),
    path('account/token/logout/', LogoutView.as_view(), name='api-logout'),
]

if settings.DEBUG:
    urlpatterns.append(path('account/token/login/',
                       TokenCreateView.as_view(), name="api-login"))
else:
    urlpatterns += [
        path('account/token/login/',
             StandAloneLoginView.as_view(), name='api-login'),
        path('account/session/', SessionView.as_view(), name='api-session'),
    ]
