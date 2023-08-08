
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static
from .views import index

schema_view = get_schema_view(
    openapi.Info(
        title="podcast_app API",
        default_version='v1',
        description="API Documentation for podcast_app App",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="developer@enfono.co.in"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


url_patterns = [
    path('', index, name='index'),
    path('api/admin/', admin.site.urls),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='docs'),
    path('api/auth/', include('user_auth.urls')),
    path('api/admin-panel/',  include('admin_panel.urls')),
    path('api/app/',  include('customer.urls'))

]


urlpatterns = url_patterns
if settings.ENVIRONMENT == 'dev':
    urlpatterns = [
        path('api_podcast_app/', include(url_patterns)),
    ]

elif settings.ENVIRONMENT == 'uat':
    urlpatterns = [
        path('uat/api_podcast_app/', include(url_patterns)),
    ]

if settings.DEBUG:
    urlpatterns += \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
