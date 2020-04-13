from django.urls import path, include

from raven.fetch.api.v1 import views as fetch_views
from raven.core.api.v1 import views as core_views

api_version = {
    'MAJOR_VERSION': 1,
    'MINOR_VERSION': 2,
    'PATCH_VERSION': 1,
}

urlpatterns = [
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
