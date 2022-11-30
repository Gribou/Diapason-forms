from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register(r'form', views.BrouillageViewSet, basename="brouillage-form")
router.register(r'postit', views.PostItViewSet, basename="brouillage-postit")
router.register(r'draft', views.DraftBrouillageViewSet,
                basename="brouillage-draft")
