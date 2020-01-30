from django.conf.urls import url, include

from raven.fetch.api.v1 import views as fetch_views
from raven.core.api.v1 import views as core_views

api_version = {
    'MAJOR_VERSION': 1,
    'MINOR_VERSION': 1,
    'PATCH_VERSION': 0,
}

urlpatterns = [
    url(
        regex='fetch/plot',
        view=fetch_views.FetchPlotDataAPIView.as_view(),
        name='fetch_plot'
    ),
    url(
        regex='fetch/stats',
        view=fetch_views.MnemonicStatisticsView.as_view(),
        name='fetch_stats'
    ),
    url(
        regex='fetch/date-range',
        view=fetch_views.FetchMnemonicDateRangeAPIView.as_view(),
        name='fetch_date_range'
    ),
    url(
        regex='fetch/min-mean-max',
        view=fetch_views.FetchMinMeanMax.as_view(),
        name='fetch_min_mean_max'
    ),
    url(
        regex='fetch',
        view=fetch_views.FetchEngineeringTelemetryAPIView.as_view(),
        name='fetch'
    ),
    url(
        regex='info',
        view=core_views.InfoAPIView.as_view(),
        name='info'
    ),
]
