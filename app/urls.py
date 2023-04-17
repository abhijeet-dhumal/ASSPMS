from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from account.views import Query

# vercel deployment changes
from django.views.static import serve
from django.conf.urls import url
from django.conf import settings

# url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}) url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})


schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="QSI"
    ),
    public=True
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('docs', schema_view.with_ui(
        'swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('query', Query.as_view(), name='query'),
    path('services/', include('services.urls')),
    path('', include('account.urls')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
               static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

