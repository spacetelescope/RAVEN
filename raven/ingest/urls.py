from django.urls import path


from . import views

urlpatterns = [
    path(
        r'execute',
        views.ExecuteIngestView.as_view(),
        name='execute'
        ),
    path(
        r'message',
        views.IngestMessageView.as_view(),
        name='message'
    ),
    path(
        r'update/schedule',
        views.UpdateIngestSchedule.as_view(),
        name='update_schedule'
    ),
    path(
        r'status',
        views.IngestStatusView.as_view(),
        name='status'
    )
]