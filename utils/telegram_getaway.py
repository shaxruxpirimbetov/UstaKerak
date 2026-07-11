from decouple import config
import requests

TELEGRAM_GATEWAY_TOKEN = config("TG_ACCESS_TOKEN")

def send_verification_code(phone_number: str, code: str = None, code_length: int = 6) -> dict:
    """
    Отправляет код подтверждения через Telegram Gateway.

    :param phone_number: номер в формате E.164, например "+998901234567"
    :param code: если передашь свой код — Telegram отправит именно его.
                 Если None — Telegram сам сгенерирует и вернёт код в ответе.
    :param code_length: длина кода, если генерирует Telegram (4-8)
    :return: dict с ответом API (там будет request_id, статус и т.д.)
    """
    url = "https://gatewayapi.telegram.org/sendVerificationMessage"

    headers = {
        "Authorization": f"Bearer {TELEGRAM_GATEWAY_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "phone_number": phone_number,
    }

    if code:
        payload["code"] = code
    else:
        payload["code_length"] = code_length

    response = requests.post(url, json=payload, headers=headers, timeout=10)
    data = response.json()

    if not data.get("ok"):
        raise Exception(f"Telegram Gateway error: {data}")

    return data["result"]


def check_verification_status(request_id: str, code: str = None) -> dict:
    """
    Проверяет статус доставки / вводимый пользователем код.
    """
    url = "https://gatewayapi.telegram.org/checkVerificationStatus"

    headers = {
        "Authorization": f"Bearer {TELEGRAM_GATEWAY_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {"request_id": request_id}
    if code:
        payload["code"] = code

    response = requests.post(url, json=payload, headers=headers, timeout=10)
    data = response.json()

    if not data.get("ok"):
        raise Exception(f"Telegram Gateway error: {data}")

    return data["result"]