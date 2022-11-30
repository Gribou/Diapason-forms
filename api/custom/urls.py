from rest_framework import routers

from .views import CustomFormViewSet, FormCategoryViewSet

router = routers.SimpleRouter()
router.register(r'form', CustomFormViewSet)
router.register(r'category', FormCategoryViewSet)
