from django.urls import path, include

from raven.fetch.api.v1 import views as fetch_views
from raven.archive.api.v1 import views as archive_views

from raven.core.api.v1 import views as core_views


api_version = {
    'MAJOR_VERSION': 2,
    'MINOR_VERSION': 3,
    'PATCH_VERSION': 0,
}

urlpatterns = [
    path(
        'fetch/msid/pagination',
        view=fetch_views.FetchFullResolutionData.as_view(),
        name='full_resolution_data'
    ),
    path(
        'archive/status/msid/count',
        view=archive_views.get_msid_count,
        name='archive_msid_count'
    ),
    path(
        'archive/status/msid/names',
        view=archive_views.get_msid_names,
        name='archive_msid_names'
    ),
    path(
        'archive/status/staged/files',
        view=archive_views.get_list_of_staged_files,
        name='archive_staged_files'
    ),
    path(
        'archive/status/ingest/history',
        view=archive_views.get_ingest_history,
        name='archive_ingest_history'
    ),
    path(
        'archive/status/ingest/files',
        view=archive_views.get_ingest_files,
        name='get_ingest_files'
    ),
    path(
        'archive/status/size',
        view=archive_views.get_archive_size,
        name='archive_size'
    ),
    path(
        'fetch/stats',
        view=fetch_views.MnemonicStatisticsView.as_view(),
        name='fetch_stats'
    ),
    path(
        'fetch/date-range',
        view=fetch_views.FetchMnemonicDateRangeAPIView.as_view(),
        name='fetch_date_range'
    ),
    path(
        'fetch',
        view=fetch_views.FetchEngineeringTelemetryAPIView.as_view(),
        name='fetch'
    ),
    path(
        'info',
        view=core_views.InfoAPIView.as_view(),
        name='info'
    ),
]
