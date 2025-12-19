import hashlib
import hmac
import json
from typing import Dict
from urllib.parse import parse_qsl

from src.infrastructure.security.exceptions import TelegramAuthError



def verify_telegram_init_data(
    init_data_raw: str,
    bot_token: str,
) -> Dict:
    # initData → list of (key, value)
    init_data = dict(parse_qsl(init_data_raw, strict_parsing=True))

    if "hash" not in init_data:
        raise TelegramAuthError("Missing hash")

    received_hash = init_data.pop("hash")

    # Формируем data_check_string
    data_check_string = "\n".join(
        f"{key}={value}"
        for key, value in sorted(init_data.items())
    )

    # Секретный ключ
    secret_key = hmac.new(
        key=b"WebAppData",
        msg=bot_token.encode(),
        digestmod=hashlib.sha256,
    ).digest()

    # Контрольный хеш
    calculated_hash = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256,
    ).hexdigest()

    if calculated_hash != received_hash:
        raise TelegramAuthError("Invalid Telegram init data")

    # user приходит строкой → в dict
    if "user" in init_data:
        init_data["user"] = json.loads(init_data["user"])

    return init_data
