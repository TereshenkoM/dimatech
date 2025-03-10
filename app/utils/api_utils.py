from hashlib import sha256

from app.core.config import settings


async def get_signature(payload):
    secret_key = settings.SECRET_KEY
    signature = sha256(
        f"{payload.account_id}{payload.amount}{payload.transaction_id}{payload.user_id}{secret_key}".encode()
    ).hexdigest()

    return signature
