from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from settings import Settings

from src.domains.user import User

def generate_jwt_token(user: User) -> str:
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(minutes=Settings().ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(user.id),
        "cpf": user.cpf,
        "email": user.email,
        "role": user.roles,
        "exp": int(expire.timestamp())
    }

    encoded_jwt = encode(payload, Settings().SECRET_KEY, algorithm=Settings().ALGORITHM)
    return encoded_jwt

def decode_jwt(token: str) -> dict:
    try:
        decoded_token = decode(token, Settings().SECRET_KEY, algorithms=[Settings().ALGORITHM])
        return decoded_token
    except ExpiredSignatureError:
        return None
    except InvalidTokenError:
        return None