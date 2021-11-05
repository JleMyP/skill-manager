from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/', include('loginas.urls')),
    path('markdownx/', include('markdownx.urls')),
    path('ht/', include('health_check.urls')),

    path('openapi/', get_schema_view(), name='openapi-schema'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),
    path('api/schema/redoc-ui/', SpectacularRedocView.as_view(url_name='schema'), name='redoc-ui'),

    path('api-auth/', include('rest_framework.urls'), name='rest-auth'),

    path('', include('apps.user.urls')),
    path('', include('apps.main.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
    urlpatterns += (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
                    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
