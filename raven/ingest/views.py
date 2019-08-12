import os
import json
import logging

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# from celery.decorators import task
# from celery.result import AsyncResult
# from celery import group

# from config.celery import app

# from kombu import Connection
# from kombu import Queue

# from celery.schedules import schedule as celery_ingest_schedule

from jeta.archive.controller import Utilities
from jeta.ingest.controller import execute

from jeta.ingest.controller import set_ingest_schedule
from jeta.ingest.controller import get_ingest_status


class UpdateIngestSchedule(APIView):

    def post(self, request, format=None):

        response = set_ingest_schedule(celery_ingest_schedule(run_every=60))

        content = {'response': response}
        return Response(json.dumps(content),
                        status=status.HTTP_200_OK,
                        content_type='application/json')


class IngestMessageView(View):

    def __init__(self):

        self.status = 202

    def get(self, request):

        with Connection('redis://') as conn:

            try:
                ingest_queue = conn.SimpleQueue('ingest_queue')
                message = ingest_queue.get(block=True, timeout=1)
                print('Received: {0}'.format(message.payload))
                message.ack()
                ingest_queue.close()
            except Exception as err:
                # print(err.args[0])
                HttpResponse(json.dumps({'error': str(err.args[0])}))

        return HttpResponse(json.dumps({'message': str(message),'payload': message.payload}), status=self.status, content_type='application/json')


class IngestStatusView(View):

    def get(self, request):

        return HttpResponse(get_ingest_status(request.GET.get('task_id', 1)), content_type='application/json')


class StopIngestView(View):

    def __init__(self):
        self.status = 202

    def post(self, request):

        self.status = 400

        return HttpResponse(json.dumps({'message': 'call not implemented'}), status=self.status, content_type='application/json')


class ExecuteIngestView(APIView):

    def post(self, request, format=None):

        try:
            Utilities.prepare_archive_on_disk()
            content = execute()
        except Exception as err:
            return HttpResponse(
                json.dumps(err.args[0]),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type='application/json')

        return HttpResponse(
            json.dumps(content),
            status=status.HTTP_200_OK,
            content_type='application/json')
