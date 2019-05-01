import json
import numpy

from datetime import datetime

from jeta.archive import fetch
from astropy.time import Time

from django.http import HttpResponse

from django.shortcuts import render
from django.views.generic import View
from django.views.generic import TemplateView

class FetchMnemonicDateRange(View):

    def get(self, request):

        mnemonic = request.GET.get('mnemonic').replace(' ', '')
        date_format = request.GET.get('dateFormat', 'iso')

        date_range = fetch.get_time_range(mnemonic, date_format)

        return HttpResponse(json.dumps({'date_range': date_range}), content_type='application/json')

class TestMnemonicData(View):

    def get(self, request):

        mnemonic = request.GET.get('mnemonic').replace(' ', '')
        start_of_doy_range = request.GET.get('start_of_doy_range', '2019:001')
        end_of_doy_range = request.GET.get('end_of_doy_range', '2019:365')

        new_domain_start = request.GET.get('newDomainStart', None)
        new_domain_end = request.GET.get('newDomainEnd', None)
        data = fetch.Msid(mnemonic, start_of_doy_range, end_of_doy_range)

        if new_domain_start is not None:

            unixStartTime = Time(new_domain_start, format="isot").unix
            unixEndTime = Time(new_domain_end, format="isot").unix

            startIndex = numpy.argwhere(data.times>unixStartTime)
            endIndex = numpy.argwhere(data.times<unixEndTime)

        times = Time(data.times, format="unix", scale='utc').iso

        times = times.tolist()
        values = data.vals.tolist()

        if new_domain_start:
            times = times[startIndex[0][0]:endIndex[-1][0]]
            values = values[startIndex[0][0]:endIndex[-1][0]]

        telemetry = [
            {
                'level': 1,
                'mnemonic': mnemonic,
                'minValue': min(data.vals),
                'maxValue': max(data.vals),
                'startTime': times[0],
                'endTime': times[-1],
                'x': times,
                'y': values,
                'type': 'scatter',
                'mode': 'lines+markers',
                'line': {'shape': 'hv'},
                'showlegend': True
            }
        ]

        return HttpResponse(json.dumps(telemetry), content_type='application/json')


class FetchTemplateView(TemplateView):

    def get(self, request):

        return render(request, 'fetch/index.html', {})
