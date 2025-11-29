import logging
from typing import Optional

import requests

from config.env import WahaSettings

logger = logging.getLogger(__name__)


class WahaClient:
    """Cliente para interagir com a API do WAHA."""

    def __init__(self, settings: Optional[WahaSettings] = None):
        self.settings = settings or WahaSettings()

    def send_message(self, chat_id: str, text: str) -> bool:
        url = f"{self.settings.base_url}/api/send/text"
        headers = {
            "X-Api-Key": self.settings.api_key,
            "Content-Type": "application/json",
        }
        payload = {
            "chatId": chat_id,
            "text": text,
            "session": self.settings.session_name,
        }
        try:
            response = requests.post(
                url, json=payload, headers=headers, timeout=self.settings.timeout_seconds
            )
            if response.status_code != 201:
                logger.error("Erro WAHA (%s): %s", response.status_code, response.text)
                return False
        except Exception as error:  # pragma: no cover - defensive logging
            logger.error("Erro ao enviar mensagem WAHA: %s", error)
            return False

        return True
