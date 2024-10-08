import requests

from config.settings import TELEGRAM_URL, BOT_TOKEN


def send_telegram_message(chat_id, message):
    """Отправка сообщения в Telegram"""

    url = f"{TELEGRAM_URL}T{BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message,
    }
    response = requests.post(url, params=params)

    if response.status_code != 200:
        raise requests.RequestException("Ошибка отправки сообщения в Telegram")
