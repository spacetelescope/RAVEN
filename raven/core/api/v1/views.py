import os
import json

from django.conf import settings
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# from raven.core.apiv1_urls import api_version as version


class InfoAPIView(APIView):

    # permission_classes = (IsAuthenticated,)

    def get(self, request, format='json'):

        from ...apiv1_urls import api_version
        import datetime

        info = dict({
            'status': 'UP',
            'info': {
               'staging_directory': os.environ['STAGING_DIRECTORY'],
               'telemetry_archive': os.environ['TELEMETRY_ARCHIVE']
            },
            'version': api_version,
            'api_access_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })

        return HttpResponse(
            json.dumps(info),
            status=status.HTTP_200_OK,
            content_type='application/json')
