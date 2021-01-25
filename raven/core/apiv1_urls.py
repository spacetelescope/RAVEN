from django.urls import path, include

from raven.fetch.api.v1 import views as fetch_views
from raven.archive.api.v1 import views as archive_views

from raven.core.api.v1 import views as core_views


api_version = {
    'MAJOR_VERSION': 1,
    'MINOR_VERSION': 7,
    'PATCH_VERSION': 2,
}

urlpatterns = [
    path(
        'archive/status/msid/count',
        view=archive_views.get_msid_count(),
        name='archive_msid_count'
    ),
    path(
        'archive/status/msid/names',
        view=archive_views.get_msid_names(),
        name='archive_msid_names'
    ),
    path(
        'archive/status/staged/files',
        view=archive_views.get_list_of_staged_files(),
        name='archive_staged_files'
    ),
    path(
        'archive/status/ingest/history',
        view=archive_views.get_ingest_history(),
        name='archive_ingest_history'
    ),
    path(
        'archive/status/size',
        view=archive_views.get_archive_size(),
        name='archive_size'
    ),
    path(
        'fetch/plot',
        view=fetch_views.FetchPlotDataAPIView.as_view(),
        name='fetch_plot'
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
        'fetch/min-mean-max',
        view=fetch_views.FetchMinMeanMax.as_view(),
        name='fetch_min_mean_max'
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
