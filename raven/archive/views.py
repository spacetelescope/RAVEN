import json
import ntpath

from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from jeta.archive import status as archive_status


class ArchiveMetrics(APIView):

    def get(self, request, format='json'):

        archive_size = archive_status.get_total_archive_area_size()
        staging_size = archive_status.get_total_archive_area_size('STAGING_DIRECTORY')
        staging_dir_stats = archive_status.staging_area_status()
        number_of_mnemonics = archive_status.get_number_of_mnemoics_in_archive()

        filenames = [ntpath.basename(paths) for paths in staging_dir_stats['files']]

        stats = dict({
            'archive_size': archive_size,
            'staging_size': staging_size,
            'staging_dir_stats': staging_dir_stats,
            'staged_files': filenames,
            'number_of_mnemonics': number_of_mnemonics,
        })

        return Response(json.dumps(stats), status=status.HTTP_200_OK, content_type="application/json")
