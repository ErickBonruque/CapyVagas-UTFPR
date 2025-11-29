from unittest.mock import MagicMock
from unittest.mock import MagicMock

from django.test import TestCase

from apps.bot.services import BotService
from apps.users.models import UserProfile


class BotServiceTests(TestCase):
    def setUp(self):
        self.waha_client = MagicMock()
        self.waha_client.settings = MagicMock(session_name="test-session")
        self.service = BotService(waha_client=self.waha_client)

    def test_handles_new_user_login_prompt(self):
        chat_id = "5511999999999@c.us"
        self.service.process_message(chat_id, "", from_me=False)

        self.waha_client.send_message.assert_called_with(
            chat_id,
            "👋 Olá! Para acessar, envie seu RA e Senha separados por espaço (Ex: a1234567 senha123).",
        )

    def test_successful_login_marks_user(self):
        chat_id = "5511999999999@c.us"
        self.service.process_message(chat_id, "123456 senha", from_me=False)

        profile = UserProfile.objects.get(phone_number=chat_id)
        self.assertTrue(profile.is_authenticated_utfpr)
        self.assertEqual(profile.ra, "123456")
        self.waha_client.send_message.assert_called_with(
            chat_id,
            "✅ Login realizado com sucesso! Digite 'vagas' para buscar oportunidades.",
        )
