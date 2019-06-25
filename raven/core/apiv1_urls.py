from django.conf.urls import url, include

from raven.fetch.api.v1 import views as fetch_views

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
        regex='fetch',
        view=fetch_views.FetchEngineeringTelemetryAPIView.as_view(),
        name='fetch'
    ),

]
