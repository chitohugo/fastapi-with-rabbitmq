from datetime import datetime, timedelta

from core.exceptions import AuthError
from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from config import settings
from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"


def create_access_token(subject: dict, expires_delta: timedelta = None) -> (str, str):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire)
    payload = {"exp": expire, **subject}
    encoded_jwt = jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)
    expiration_datetime = expire.strftime(settings.datetime_format)
    return encoded_jwt, expiration_datetime


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, settings.secret_key, algorithms=ALGORITHM)
        return decoded_token if decoded_token["exp"] >= int(round(datetime.utcnow().timestamp())) else None
    except Exception:
        return {}


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise AuthError(message="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise AuthError(message="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise AuthError(message="Invalid authorization code.")

    def verify_jwt(self, jwt_token: str) -> bool:
        is_token_valid: bool = False
        try:
            payload = decode_jwt(jwt_token)
        except Exception:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid
