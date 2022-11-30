from django.urls import path, include
from djoser.views import UserViewSet
from django.conf import settings

from efne.urls import router as fne_router
from similitude.urls import router as simi_router
from brouillage.urls import router as brouillage_router
from custom.urls import router as custom_router

from .routers import NestedDefaultRouter
from .views import ConfigViewSet, CounterViewSet, FormsMetaViewSet, HealthCheckView


router = NestedDefaultRouter()
router.register(r'profile', UserViewSet)
router.register(r'config', ConfigViewSet, basename="config")
router.register(r'counters', CounterViewSet, basename="counters")
router.register(r'meta', FormsMetaViewSet, basename="meta")
router.register_nested_router("fne", fne_router)
router.register_nested_router("similitude", simi_router)
router.register_nested_router("brouillage", brouillage_router)
router.register_nested_router("custom", custom_router)
router.register_additional_view("sso-login", 'api-sso-login')
router.register_additional_view("sso-login-callback", 'api-sso-login-complete')
router.register_additional_view("login", "api-login")
router.register_additional_view("logout", "api-logout")
router.register_additional_view("permissions", "api-permissions")
router.register_additional_view("health", "api-health")

if not settings.DEBUG:
    router.register_additional_view("session", "api-session")

urlpatterns = [
    path('', include('sso.urls')),
    path('', include(router.urls)),
    path('health/', HealthCheckView.as_view(),
         name="api-health"),
]
