import os
import json

from django.http import HttpResponse

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class InfoAPIView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

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
