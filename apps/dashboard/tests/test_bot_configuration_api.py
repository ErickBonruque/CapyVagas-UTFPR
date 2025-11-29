from django.test import TestCase
from rest_framework.test import APIClient

from apps.bot.models import BotConfiguration


class BotConfigurationApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_active_endpoint_returns_defaults(self):
        response = self.client.get("/api/bot/configuration/active/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["waha_url"], "http://localhost:3000")
        self.assertEqual(payload["waha_api_key"], "dev-api-key")
        self.assertEqual(payload["waha_session"], "dev-session")
        self.assertEqual(payload["dashboard_username"], "admin")

    def test_create_replaces_previous_configuration(self):
        BotConfiguration.objects.create(
            waha_url="http://old", waha_api_key="old", waha_session="old", dashboard_username="old", dashboard_password="old"
        )

        response = self.client.post(
            "/api/bot/configuration/",
            {
                "waha_url": "http://new",
                "waha_api_key": "new-key",
                "waha_session": "new-session",
                "dashboard_username": "new-user",
                "dashboard_password": "new-pass",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(BotConfiguration.objects.count(), 1)
        active = BotConfiguration.objects.first()
        self.assertEqual(active.waha_url, "http://new")
        self.assertEqual(active.waha_api_key, "new-key")
        self.assertEqual(active.waha_session, "new-session")
        self.assertEqual(active.dashboard_username, "new-user")
