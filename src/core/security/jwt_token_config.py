import jwt
import datetime
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer

from src.core.error.error_type_code import EXCEPTION_TYPE
from src.core.util.core_util import get_secret_data

SECRET_DATA = get_secret_data()
SECRET_KEY = SECRET_DATA['secret_key']
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_jwt_access_token(login_id: str, user_id: int):
    return __create_jwt_token(login_id, user_id, datetime.datetime.utcnow() + datetime.timedelta(minutes=5))


def create_jwt_refresh_token(login_id: str, user_id: int):
    return __create_jwt_token(login_id, user_id, datetime.datetime.utcnow() + datetime.timedelta(days=30))


def __create_jwt_token(login_id: str, user_id: int, expiration):
    payload = {"login_id": login_id, "user_id": user_id, "exp": expiration}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def decode_jwt_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(status_code=EXCEPTION_TYPE.ERROR_402.value["code"], detail=EXCEPTION_TYPE.ERROR_402.value["message"])
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=EXCEPTION_TYPE.ERROR_422.value["code"], detail=EXCEPTION_TYPE.ERROR_422.value["message"])


def get_current_user_id(token: str = Depends(oauth2_scheme)):
    return decode_jwt_token(token).get("user_id")


def get_current_user_login_id(token: str = Depends(oauth2_scheme)):
    return decode_jwt_token(token).get("login_id")


def verify_token(credentials: [HTTPAuthorizationCredentials, None] = Depends(HTTPBearer())):
    # 토큰 검증 로직 수행
    token = credentials.credentials
    decode_jwt_token(token)
    return token