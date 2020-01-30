import os
import json

from django.conf import settings
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework import status

# from raven.core.apiv1_urls import api_version as version

class InfoAPIView(APIView):


    def get(self, request, format='json'):

        from ...apiv1_urls import api_version

        info = dict({
            'info': {
               'staging_directory': os.environ['STAGING_DIRECTORY'],
               'telemetry_archive': os.environ['TELEMETRY_ARCHIVE']
            },
            'version': api_version
        })

        return HttpResponse(
            json.dumps(info),
            status=status.HTTP_200_OK,
            content_type='application/json')
