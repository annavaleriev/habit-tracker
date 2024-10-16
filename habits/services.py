import requests

from config.settings import TELEGRAM_URL, BOT_TOKEN


def send_telegram_message(chat_id, message):
    """Отправка сообщения в Telegram"""

    url = f"{TELEGRAM_URL}{BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message,
    }
    requests.get(url, params=params)
