from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.FetchTemplateView.as_view(), name='data_viewer'),
    url(r'data', views.TestMnemonicData.as_view(), name='data'),
    url(r'date-range', views.FetchMnemonicDateRange.as_view(), name='date_range'),
    url(r'stats', views.MnemonicStatisticsView.as_view(), name='stats'),
]