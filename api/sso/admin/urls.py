from django.urls import path

from .views import AdminLoginView, AdminLoginCompleteView, AdminLogoutView

app_name = "sso"
urlpatterns = [
    path('login/', AdminLoginView.as_view(), name="login"),
    path('login/callback/', AdminLoginCompleteView.as_view(), name="login-complete"),
    path('logout/', AdminLogoutView.as_view(), name="logout")
]
