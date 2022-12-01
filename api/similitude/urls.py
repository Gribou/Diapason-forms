from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register(r'form', views.SimiViewSet)
router.register(r'postit', views.PostItViewSet)
router.register(r'draft', views.DraftSimiViewSet)
