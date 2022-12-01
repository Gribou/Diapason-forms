from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register(r'form', views.FneViewSet, basename='fne-form')
router.register(r'postit', views.PostItViewSet, basename='fne-postit')
router.register(r'attachment', views.AttachmentViewSet,
                basename='fne-attachment')
router.register(r'draft', views.DraftFneViewSet, basename='fne-draft')
