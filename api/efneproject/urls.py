from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, reverse
from django.views.generic import TemplateView, RedirectView
from django.views.decorators.cache import never_cache
from django.shortcuts import redirect

react_frontend = never_cache(TemplateView.as_view(template_name="index.html"))

urlpatterns = [
    path('sso/', include('sso.admin.urls')),
    path('admin/logout/', lambda request: redirect(reverse('sso:logout'),
         permanent=False)),  # uses SSO logout in admin
    path('admin/', admin.site.urls),
    path('admin', RedirectView.as_view(pattern_name='admin:index',
         permanent=False)),  # force trailing slash
    path('api', RedirectView.as_view(pattern_name='api-root',
         permanent=False)),  # force trailing slash
    path('api/', include('api.urls')),
    path('', react_frontend, name="home"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]

# service react index page for anything else
urlpatterns.append(path('<path:path>', react_frontend))
