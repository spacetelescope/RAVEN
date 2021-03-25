from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views
from django.contrib import admin


urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),
    path(
        'ingest/',
        include(
            ('raven.ingest.urls', 'ingest'),
            namespace='ingest')
        ),
    path(
        'archive/',
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
        'api-token-auth/',
        views.obtain_auth_token
    )
]

urlpatterns = format_suffix_patterns(urlpatterns)
