from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib import admin

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path(r'^admin/', admin.site.urls),
    path(
        r'^ingest/',
        include(
            ('raven.ingest.urls', 'ingest'),
            namespace='ingest')
        ),
    path(
        r'^archive/',
        include(
            ('raven.archive.urls', 'archive'),
            namespace='archive')
        ),
    path(
        r'api/v1/',
        include(
            ('raven.core.apiv1_urls', 'core'),
            namespace='apiv1')
        ),
    path(
        'api/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'api/token/verify/',
        TokenVerifyView.as_view(),
        name='token_verify'
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
