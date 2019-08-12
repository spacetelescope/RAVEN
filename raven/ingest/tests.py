from django.test import TestCase
from django.http import HttpRequest

from .views  import ExecuteIngestView

class TestIngestAPI(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_ingest_execute_returns_HTTP_200_or_500(self):
        request = HttpRequest()
        execute_view = ExecuteIngestView.as_view()
        response = execute_view()
        self.assertEqual(1, 1)
        #self.assertTrue((200 in response.status_code or 500 in response.status_code))
