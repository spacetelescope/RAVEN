import datetime
from datetime import timedelta

from django.conf import settings


def provide_default_date_range(dictionary):

    """ A function used to provide default values for start/end yday

    Call Args:
        dictionary a dict() with assumed keys for start_yday and end_yday

    Returns:
        start_yday, end_yday
    """

    tomorrow = datetime.datetime.now() + timedelta(days=1)
    default_end_ydoy = f"{tomorrow.timetuple().tm_year}:{tomorrow.timetuple().tm_yday}:00:00:00.000"

    try:
        start_yday = dictionary.GET.get('start_yday', '')
        end_yday = dictionary.GET.get('end_yday', '')
    except Exception as err:
        raise err.args[0]

    if start_yday == '':
        start_yday = '2008:001:00:00:00.000'
    if end_yday == '':
        end_yday = default_end_ydoy

    return start_yday, end_yday
