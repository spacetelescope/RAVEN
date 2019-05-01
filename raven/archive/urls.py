from django.conf.urls import url


from . import views

urlpatterns = [
    url(
        r'metrics',
        views.ArchiveMetrics.as_view(),
        name='metrics'
        ),
]
