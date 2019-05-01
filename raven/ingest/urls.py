from django.conf.urls import url


from . import views

urlpatterns = [
    url(
        r'execute',
        views.ExecuteIngestView.as_view(),
        name='execute'
        ),
    url(
        r'message',
        views.IngestMessageView.as_view(),
        name='message'
    ),
    url(
        r'update-schedule',
        views.UpdateIngestSchedule.as_view(),
        name='update_schedule'
    ),
    url(
        r'status',
        views.IngestStatusView.as_view(),
        name='status'
    )
]