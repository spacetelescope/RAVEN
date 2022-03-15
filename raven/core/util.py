import datetime
from datetime import timedelta

from django.conf import settings


def provide_default_date_range(request):

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
