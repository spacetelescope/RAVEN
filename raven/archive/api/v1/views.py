import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from jeta.archive import status as archive_status


@api_view(http_method_names=['GET'])
def get_msid_count(request):
    """ A function to get the current count of msids managed in the archive
    """
    try:
        msid_count = archive_status.get_msid_count()
    except Exception as err:
        return Response(
            json.dumps({'error': err.args[0]}),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content_type='application/json'
        )

    return Response(
        json.dump({'count': msid_count}),
        status=status.HTTP_200_OK,
        content_type='application/json'
    )


@api_view(http_method_names=['GET'])
def get_msid_names(request):
    """ A function to get a list of msids names managed in the archive
    """
    try:
        msid_names = archive_status.get_msid_names()
    except Exception as err:
        return Response(
            json.dumps({'error': err.args[0]}),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content_type='application/json'
        )

    return Response(
        json.dump({'msids': msid_names}),
        status=status.HTTP_200_OK,
        content_type='application/json'
    )


@api_view(http_method_names=['GET'])
def get_list_of_staged_files(request):
    """ A function to get a list of ingest files staged in the archive
    """
    try:
        staged_files = archive_status.get_list_of_staged_files()
    except Exception as err:
        return Response(
            json.dumps({'error': err.args[0]}),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content_type='application/json'
        )

    return Response(
        json.dump({'staged_files': staged_files}),
        status=status.HTTP_200_OK,
        content_type='application/json'
    )


@api_view(http_method_names=['GET'])
def get_ingest_history(request):
    """ A function to get metadata about ingest history
    """
    try:
        ingest_history = archive_status.get_ingest_history()
    except Exception as err:
        return Response(
            json.dumps({'error': err.args[0]}),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content_type='application/json'
        )

    return Response(
        json.dump({'ingest_history': ingest_history}),
        status=status.HTTP_200_OK,
        content_type='application/json'
    )


@api_view(http_method_names=['GET'])
def get_archive_size(area, include_backlog=False):
    """ A function to get the size (in bytes) on disk of either the staging
    area or tlm archive
    """
    return 0
