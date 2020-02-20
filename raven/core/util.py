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

    # Default start_yday should be a configurable epic

    try:
        start_yday = dictionary.GET.get('start_yday', '2008:001:00:00:00.000')
        end_yday = dictionary.GET.get('end_yday', '2021:001:00:00:00.000')
    except Exception as err:
        raise

    return start_yday, end_yday
