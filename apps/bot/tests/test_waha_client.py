from unittest.mock import patch

from django.test import TestCase

from config.env import WahaSettings
from infra.waha.client import WahaClient


class WahaClientTests(TestCase):
    def test_send_message_success(self):
        settings = WahaSettings(base_url="http://localhost:3000", api_key="token", session_name="session")
        client = WahaClient(settings=settings)

        with patch("infra.waha.client.requests.post") as post_mock:
            post_mock.return_value.status_code = 201
            result = client.send_message("5511999999999@c.us", "hello")

        self.assertTrue(result)
        post_mock.assert_called_once()

    def test_send_message_failure_logs_error(self):
        client = WahaClient()

        with patch("infra.waha.client.requests.post") as post_mock:
            post_mock.return_value.status_code = 500
            result = client.send_message("5511999999999@c.us", "hello")

        self.assertFalse(result)
