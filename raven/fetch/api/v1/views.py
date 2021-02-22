import json
import datetime
from datetime import timedelta

import requests
import numpy as np

from django.http import HttpResponse
from django.urls import reverse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from astropy.time import Time

from jeta.archive import fetch

from raven.core.util import provide_default_date_range


class FetchMinMeanMax(APIView):

    def get(self, request, format='json'):

        try:
            mnemonic = request.GET.get('mnemonic', None)
            start_yday, end_yday = provide_default_date_range(request)
            interval = request.GET.get('interval', '5min')

            mmenmonic_stats = fetch.MSID(
                                            mnemonic,
                                            start_yday,
                                            end_yday,
                                            stat=interval
                                        )

            stats = {
                        'values': mmenmonic_stats.vals.tolist(),
                        'times': Time(
                            mmenmonic_stats.times.tolist(),
                            format="cxcsec",
                            scale='utc').iso.tolist(),
                        'mins': mmenmonic_stats.mins.tolist(),
                        'means': mmenmonic_stats.means.tolist(),
                        'maxes': mmenmonic_stats.maxes.tolist(),
                        'tstart': mmenmonic_stats.tstart
            }

        except (ValueError, IOError, Exception) as err:
            self.message = err.args[0]
            return HttpResponse(
                json.dumps(
                    {
                        'message': self.message,
                        'interval': interval,
                        'start_yday': start_yday,
                        'end_yday': end_yday,
                        'class': 'FetchMinMeanMax',
                        'source': 'raven.api.v1'
                    }
                ),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type='application/json'
            )

        return HttpResponse(json.dumps(
                {
                    'start_yday': start_yday,
                    'end_yday': end_yday,
                    'interval': interval,
                    'data': stats
                }
            ),
            status=status.HTTP_200_OK,
            content_type='application/json'
        )


class FetchMnemonicDateRangeAPIView(APIView):

    """ APIView to fetch the range of dates a given mnemonic has data in the archive.

        NOTE: View only implements the HTTP GET method. All other calls should return 405.
    """

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


class FetchPlotDataAPIView(APIView):

    """ APIView to to return data and meta-data for rendering plotly
        plots.
    """

    def get(self, request, format='json'):

        mnemonic = request.GET.get('mnemonic', None)
        fetch_url = request.build_absolute_uri(reverse('apiv1:fetch'))

        tomorrow = datetime.datetime.now() + timedelta(days=1)
        default_end_ydoy = f"{tomorrow.timetuple().tm_year}:{tomorrow.timetuple().tm_yday}:00:00:00.000"

        start_of_ydoy = request.GET.get('start_of_range')

        end_of_ydoy = request.GET.get(
            'end_of_range',
            default_end_ydoy
        )

        try:
            response = requests.get(fetch_url, params={
                    'mnemonic': mnemonic,
                    'start_of_ydoy': start_of_ydoy,
                    'end_of_ydoy': end_of_ydoy
            })

            plot_data = response.json()
            plot_data[0]['type'] = 'scattergl'
            plot_data[0]['mode'] = 'lines+markers'

            plot_data[0]['line'] = {
                    'shape': 'hv',
                    'color': 'rgb(30, 110, 162)'
            }

            plot_data[0]['showlegend'] = True

        except Exception as err:
            return HttpResponse(
                json.dumps({
                        'message': err.args[0],
                        'source': 'raven.api',
                        'class': 'FetchPlotDataAPIView',
                    },
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type='application/json')

        return Response(
            plot_data,
            status=status.HTTP_200_OK,
            content_type='application/json')


class MnemonicStatisticsView(APIView):

    """ APIView to to return data and meta-data for rendering plotly
        plots.
    """

    def get(self, request, format='json'):

        try:
            mnemonic = request.GET.get('mnemonic', None)
            start_yday, end_yday = provide_default_date_range(request)
            interval = request.GET.get('interval', '5min')

            mmenmonic_stats = fetch.MSID(mnemonic, start_yday, end_yday, stat=interval)

            stats = {
                'indexes': mmenmonic_stats.indexes.tolist(),
                'times': Time(mmenmonic_stats.times.tolist(), format="cxcsec", scale='utc').iso.tolist(),
                'values': mmenmonic_stats.vals.tolist(),
                'mins': mmenmonic_stats.mins.tolist(),
                'maxes': mmenmonic_stats.maxes.tolist(),
                'means': mmenmonic_stats.maxes.tolist(),
                'midvals':  mmenmonic_stats.midvals.tolist(),
            }

        except Exception as err:
            return HttpResponse(
                            json.dumps({
                                'error': err.args[0],
                                'source': 'raven.api',
                                'class': 'MnemonicStatisticsView',
                            }),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content_type='application/json'
                   )

        return HttpResponse(json.dumps({'stats' : stats}), status=status.HTTP_200_OK, content_type='application/json')
