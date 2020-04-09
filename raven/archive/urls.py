from django.urls import path


from . import views

urlpatterns = [
    path(
        r'metrics',
        views.ArchiveMetrics.as_view(),
        name='metrics'
    ),
]
