import json
import numpy
import datetime
from datetime import timedelta

import requests

from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework import status

from astropy.time import Time

from jeta.archive import fetch


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

        tomorrow = datetime.datetime.now() + timedelta(days=1)
        mnemonic = request.GET.get('mnemonic').replace(' ', '').upper()

        default_end_doy = f"{tomorrow.timetuple().tm_year}:{tomorrow.timetuple().tm_yday}"

        start_of_doy_range = request.GET.get('start_doy', '2010:001')
        end_of_doy_range = request.GET.get(
            'end_doy',
            default_end_doy)

        try:
            data = fetch.Msid(mnemonic, start_of_doy_range, end_of_doy_range)
            times = Time(data.times, format="unix", scale='utc').iso.tolist()
            values = data.vals.tolist()
            telemetry = [
                {
                    'levelOfDetail': 1,
                    'mnemonic': mnemonic,
                    'minValue': data.vals.min(),
                    'maxValue': data.vals.max(),
                    'startTime': times[0],
                    'endTime': times[-1],
                    'x': times,
                    'y': values,
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
                json.dumps({'message': err.args[0]}),
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

        fetch_url = request.build_absolute_uri(reverse('apiv1:fetch'))

        mnemonic = request.GET.get('mnemonic', None)

        try:
            response = requests.get(fetch_url, params={'mnemonic': mnemonic})

        except Exception as err:
            return HttpResponse(
                json.dumps({'message': err.args[0]}),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type='application/json')

        plot_data = response.json()
        plot_data[0]['type'] = 'scattergl'
        plot_data[0]['mode'] = 'lines+markers'
        plot_data[0]['line'] = {
                    'shape': 'hv',
                    'color': 'rgb(0, 50, 250)'
                }
        plot_data[0]['showlegend'] = True

        return HttpResponse(
            json.dumps(plot_data),
            status=status.HTTP_200_OK,
            content_type='application/json')


class MnemonicStatisticsView(APIView):

    """ APIView to to return data and meta-data for rendering plotly
        plots.
    """
    def get(self, request, format='json'):

        mnemonic = request.GET.get('mnemonic', None)
        interval = request.GET.get('interval', '5min')

        try:
            stats, group = fetch.read_stats_file(mnemonic, interval)

        except Exception as err:

            return HttpResponse(
                json.dumps({'message': err.args[0]}),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type='application/json')

        return HttpResponse(
            json.dumps({'stats': stats}),
            status=status.HTTP_200_OK,
            content_type='application/json')
