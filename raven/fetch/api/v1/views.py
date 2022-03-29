from ctypes import sizeof
from io import StringIO
import os
import sys
import csv
import json
import datetime
from datetime import timedelta

import requests
import numpy as np
import pandas as pd

from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.urls import reverse

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from astropy.time import Time

from jeta.archive import fetch
from jeta.archive.files import ValueFile, TimeFile

from raven.core.util import provide_default_date_range


class FetchFullResolutionData(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def default_date_range(self, request):

        """ A function used to provide default values for start/end yday

        Call Args:
            dictionary a dict() with assumed keys for tstart and tstop

        Returns:
            tstart, tstop
        """
        tstart = request.GET.get('tstart', None)
        tstop = request.GET.get('tstop', None)
    
        if tstart == '':
            # Set tstart to launch epoch by default
            tstart = '2021:358:00:00:00.000'
        if tstop == '':
            # Set tstop to the start of the next day by default
            tomorrow = datetime.datetime.now() + timedelta(days=1)
            tstop = f'{tomorrow.timetuple().tm_year}:{tomorrow.timetuple().tm_yday:03d}:00:00:00.000'

        return tstart, tstop

    def get(self, request, format='json'):

        try:
            msid = request.GET.get('msid')
            draw = request.GET.get('draw')
            idx0 = int(request.GET.get('start', 0))
            length = int(request.GET.get('length'))
    
            tstart, tstop = self.default_date_range(request) 

            vf = ValueFile(msid)
            tf = TimeFile(msid)

            vf.get_file_data_range(
                Time(tstart, format='yday').jd, 
                Time(tstop, format='yday').jd
            )
            tf.get_file_data_range(
                Time(tstart, format='yday').jd, 
                Time(tstop, format='yday').jd
            )

            # return to client
            data  = list(zip(Time(tf.selection[idx0:idx0+length], format='jd').yday, vf.selection[idx0:idx0+length]))
            filtered_records = vf.selection_length - len(data) 

        except Exception as err:
            return HttpResponse(
                            json.dumps({'error': err.args[0]}),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content_type='application/json'
                   )
        return HttpResponse(
                        json.dumps(
                            {
                                'data': data, 
                                'recordsTotal': vf.selection_length, 
                                'recordsFiltered': filtered_records,
                                'draw': draw
                            }),
                        status=status.HTTP_200_OK,
                        content_type='application/json'
               )


class FetchMnemonicDateRangeAPIView(APIView):

    """ APIView to fetch the range of dates a given mnemonic has data in the archive.

        NOTE: View only implements the HTTP GET method. All other calls should return 405.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format='json'):

        """ HTTP GET method implementation for fetching the date range.

        Call Args:
            mnemonic (str): The mnemonic for which the date range is
                being requested.
            dateFormat (str): The string format of the dates returned.

        Returns:
            HTTP_200_OK: a json object with key `date_range` with a list value
                containing the start and end datetimes for the mnemonic.
            HTTP_500_INTERNAL_SERVER_ERROR: a json object with key `error`
                with a string value set to the error message for the exception.
        """

        mnemonic = request.GET.get('mnemonic').replace(' ', '')
        date_format_specifier = request.GET.get('dateFormatSpecifier', 'iso')

        try:
            mnemonic_archive_date_range = fetch.get_time_range(
                                                mnemonic,
                                                date_format_specifier)

        except Exception as err:
            return HttpResponse(
                            json.dumps({'error': err.args[0]}),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content_type='application/json'
                   )

        return HttpResponse(
                        json.dumps({'date_range': mnemonic_archive_date_range}),
                        status=status.HTTP_200_OK,
                        content_type='application/json'
               )


class FetchEngineeringTelemetryAPIView(APIView):

    """ APIView to fetch the range of dates a given mnemonic has data in the archive.

        NOTE: View only implements the HTTP GET method. All other calls should return 405.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def validate_input_date_range(self, request):

        tomorrow = datetime.datetime.now() + timedelta(days=1)
        default_end_ydoy = f"{tomorrow.timetuple().tm_year}:{tomorrow.timetuple().tm_yday:03d}:00:00:00.000"

        start_of_ydoy = request.GET.get('start_of_ydoy')
        end_of_ydoy = request.GET.get('end_of_ydoy', '')

        if start_of_ydoy is None or start_of_ydoy == '' or start_of_ydoy == 'None':
            start_of_ydoy = '2008:001:00:00:00.000'

        if end_of_ydoy == '' or end_of_ydoy is None:
            end_of_ydoy = default_end_ydoy

        return start_of_ydoy, end_of_ydoy

    def validate_fetched_times(self, times):

        self.start_time = ''
        self.end_time = ''

        iso_times = []

        if len(times) != 0:
            iso_times = Time(times, format="unix", scale='utc').iso.tolist()
            self.start_time = iso_times[0]
            self.end_time = iso_times[-1]

        return iso_times

    def validate_fetched_values(self, values):

        min_value = None
        max_value = None

        if len(values) != 0:
            min_value = values.min(),
            max_value = values.max(),
        return [min_value, max_value]

    def zoom(self, request, data):

        """ APIView to handling zooming in on plots.
        """
        pass
        # start_isot = request.GET.get('startISOT', None)
        # end_isot = request.GET.get('endISOT', None)

        # unix_start_time = Time(start_isot, format="isot").unix
        # unix_end_time = Time(end_isot, format="isot").unix

        # startIndex = numpy.argwhere(data.times>unix_start_time)
        # endIndex = numpy.argwhere(data.times<unix_end_time)

        # times = times[startIndex[0][0]:endIndex[-1][0]]
        # values = values[startIndex[0][0]:endIndex[-1][0]]

    def fetch(self, request):

        """ HTTP GET method implementation fetching telemetry data.

            Call Args:
                mnemonic (str): The mnemonic for which the data is being requested.

        Returns:
            HTTP_200_OK: a json object with key/value pairs.
                containing the start and end datetimes for the mnemonic.
            HTTP_500_INTERNAL_SERVER_ERROR: a json object with key `error`
                with a string value set to the error message for the exception.
        """
        telemetry = None
        mnemonic = request.GET.get('mnemonic').replace(' ', '').upper()

        start_of_ydoy, end_of_ydoy = self.validate_input_date_range(request)

        try:

            msid = fetch.Msid(mnemonic, start_of_ydoy, end_of_ydoy)

            if len(msid) > 50_000:
                interval = np.round(np.linspace(0, len(msid) - 1, 50_000)).astype(int)

                plot_x = msid.times[interval]
                plot_y = msid.vals[interval]

                plot_x = self.validate_fetched_times(plot_x)
                min_max_values = self.validate_fetched_values(plot_y)
                plot_y = plot_y.tolist()
            else:
                plot_x = self.validate_fetched_times(msid.times)
                min_max_values = self.validate_fetched_values(msid.vals)
                plot_y = msid.vals.tolist()

            data_length = len(plot_y)

            telemetry = [
                {
                    'levelOfDetail': 1,
                    'mnemonic': mnemonic,
                    'length': data_length,
                    'minValue': min_max_values[0],
                    'maxValue': min_max_values[1],
                    'startTime': self.start_time,
                    'endTime': self.end_time,
                    'x': plot_x,
                    'y': plot_y,
                }
            ]

        except Exception as err:
            raise err

        return telemetry

    def get(self, request):

        try:
            telemetry = self.fetch(request)

        except Exception as err:

            return HttpResponse(
                json.dumps({
                    'message': err.args[0],
                    'source': 'raven.api',
                    'class': 'FetchEngineeringTelemetryAPIView',
                }),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type='application/json')

        return HttpResponse(
            json.dumps(telemetry),
            status=status.HTTP_200_OK,
            content_type='application/json'
            )

class MnemonicStatisticsView(APIView):

    """ APIView to to return data and meta-data for rendering plotly
        plots.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_data(self, stats, interval):
        if interval == '5min':
            return {
                    'indexes': stats.indexes.tolist(),
                    'times': Time(stats.times.tolist(), format="unix", scale='utc').yday.tolist(),
                    'values': stats.vals.tolist(),
                    'mins': stats.mins.tolist(),
                    'maxes': stats.maxes.tolist(),
                    'means': stats.maxes.tolist(),
                    'midvals': stats.midvals.tolist(),
                }
        if interval == 'daily':
            return {
                'times': Time(stats.times.tolist(), format="unix", scale='utc').yday.tolist(),
                'mins': stats.mins.tolist(),
                'maxes': stats.maxes.tolist(),
                'means': stats.maxes.tolist(),
                'stds': stats.stds.tolist(),
                'p01s': stats.p01s.tolist(),
                'p05s': stats.p05s.tolist(),
                'p16s': stats.p16s.tolist(),
                'p50s': stats.p50s.tolist(),
                'p84s': stats.p84s.tolist(),
                'p95s': stats.p95s.tolist(),
                'p99s': stats.p99s.tolist()
            }

    def get(self, request, format='json'):
        """ HTTP get method controller to handle fetch requests for msid stats
        """

        try:
            msid = request.GET.get('msid', None)
            tstart, tstop = provide_default_date_range(request)
            interval = request.GET.get('interval')
            if interval == '':
                interval = '5min'

            stats = fetch.MSID(msid, tstart, tstop, stat=interval)
            stats = self.get_data(stats, interval)

        except (Exception, ValueError) as err:
            return HttpResponse(
                            json.dumps({
                                'error': "Failed to fetch data for {}. Reason: {}".format(msid ,err.args[0]),
                                'source': 'raven.api',
                                'class': 'MnemonicStatisticsView',
                                'tstart': tstart,
                                'tstop': tstop
                            }),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content_type='application/json'
                   )

        return HttpResponse(json.dumps({'stats' : stats, 'interval': interval, 'tstart': tstart, 'tstop': tstop}), status=status.HTTP_200_OK, content_type='application/json')

class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

class FetchDownloadView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def download(self, request, file_path):
        header = False
        if request.GET.get('interval') != 'full':
            data_buffer = StringIO()
            for line in self.get_data(request=request):
                if line:
                    print(line, file=data_buffer)

            response = StreamingHttpResponse((row for row in data_buffer.getvalue()),
                                                content_type="text/csv")
            response['Content-Disposition'] = f'attachment; filename="{file_path}"'
                # response['Content-Length'] = sys.getsizeof(rows)
            return response
        else:
            data = self.get_data(request=request)
            pseudo_buffer = Echo()
            writer = csv.writer(pseudo_buffer)
            response = StreamingHttpResponse((writer.writerow(str(row).replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('\'', '').split(',')) for row in data),
                                            content_type="text/csv")
            response['Content-Disposition'] = f'attachment; filename="{file_path}"'
            # response['Content-Length'] = (sizeof(float) + sizeof(int)) * len(data)
            return response
       
       

    def get_data(self, request):

        self.tstart, self.tstop = provide_default_date_range(request)
       
        if self.interval == 'full':
            self.data = fetch.MSID(self.msid, self.tstart, self.tstop)
            return list(zip(Time(self.data.times.tolist(), format="unix", scale='utc').yday.tolist(), self.data.vals))

        if self.interval == '5min': 
            self.data = fetch.MSID(self.msid, self.tstart, self.tstop, stat=self.interval)
            stats = {
                        'times': Time(self.data.times.tolist(), format="unix", scale='utc').yday.tolist(),
                        'values': self.data.vals.tolist(),
                        'mins': self.data.mins.tolist(),
                        'maxes': self.data.maxes.tolist(),
                        'means': self.data.maxes.tolist(),
                        'midvals': self.data.midvals.tolist(),
                    }
        if self.interval == 'daily':
            self.data = fetch.MSID(self.msid, self.tstart, self.tstop, stat=self.interval)
            stats = {
                    'times': Time(self.data.times.tolist(), format="unix", scale='utc').yday.tolist(),
                    'mins': self.data.mins.tolist(),
                    'maxes': self.data.maxes.tolist(),
                    'means': self.data.maxes.tolist(),
                    'stds': self.data.stds.tolist(),
                    'p01s': self.data.p01s.tolist(),
                    'p05s': self.data.p05s.tolist(),
                    'p16s': self.data.p16s.tolist(),
                    'p50s': self.data.p50s.tolist(),
                    'p84s': self.data.p84s.tolist(),
                    'p95s': self.data.p95s.tolist(),
                    'p99s': self.data.p99s.tolist()
                }
        return stats
            
    def get(self, request):
        self.msid = request.GET.get('msid', None)
        self.interval = request.GET.get('interval')
        if self.interval not in ['full', '5min', 'daily']:
            return HttpResponse(
                json.dumps({'error': f'{self.interval} is not a valid interval'}), 
                status=400, 
                content_type='application/json'
            )
        file_path = '{}_{}_{}.csv'.format(str(self.msid).lower(), Time.now().unix, self.interval)

        return self.download(request=request, file_path=file_path)
