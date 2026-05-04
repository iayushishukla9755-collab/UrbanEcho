from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="TestDB API",
        default_version='v1',
        description="CRUD API for Department & Employee",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # App URLs
    path('api/', include('public_issue.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', include('public_issue.urls')),
]

# Serve media files in both development and production
if settings.DEBUG or True:  # Serve media files in production too
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

