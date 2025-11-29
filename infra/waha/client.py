import os
import requests
import logging

logger = logging.getLogger(__name__)

class WahaClient:
    """
    Cliente para interagir com a API do WAHA.
    """
    def __init__(self):
        self.base_url = os.environ.get('WAHA_URL', 'http://waha:3000')
        self.api_key = os.environ.get('WAHA_API_KEY', '')
        self.session = os.environ.get('WAHA_SESSION_NAME', 'default')

    def send_message(self, chat_id, text):
        url = f'{self.base_url}/api/send/text'
        headers = {
            'X-Api-Key': self.api_key,
            'Content-Type': 'application/json',
        }
        payload = {
            'chatId': chat_id,
            'text': text,
            'session': self.session
        }
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=5)
            if response.status_code != 201:
                logger.error(f"Erro WAHA: {response.text}")
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem WAHA: {e}")
