from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.api.guest import dao as guest_dao
from src.api.guest.request_dto import UserLoginDto, UserSignUpDto
from src.api.guest.response_dto import UserTokenDto
from src.core.database.domain import User, SignUpHistory, EmailVerificationRequest
from src.core.error.error_type_code import EXCEPTION_TYPE
from src.core.security.jwt_token_config import decode_jwt_token, create_jwt_access_token, create_jwt_refresh_token
from src.core.util.core_util import hash_function, get_seoul_datetime_format, generate_random_string
from src.core.util import database_util


def get_user_detail_by_login_id(login_id: str, db: Session):
    user = guest_dao.find_user_by_login_id(login_id, db)
    if user is None:
        raise HTTPException(status_code=EXCEPTION_TYPE.ERROR_505.value["code"], detail=EXCEPTION_TYPE.ERROR_505.value["message"])
    return user


def get_user_detail_by_email(email: str, db: Session):
    user = guest_dao.find_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=EXCEPTION_TYPE.ERROR_505.value["code"], detail=EXCEPTION_TYPE.ERROR_505.value["message"])
    return user


def get_user_login_id_by_email(email: str, db: Session):
    login_id = guest_dao.find_user_login_id_by_email(email, db)
    if login_id is None:
        raise HTTPException(status_code=EXCEPTION_TYPE.ERROR_505.value["code"], detail=EXCEPTION_TYPE.ERROR_505.value["message"])
    return login_id


def check_duplicate_nickname(nickname: str, db: Session):
    user = guest_dao.find_user_by_nickname(nickname, db)
    return 1 if user else 0


def check_duplicate_email(email: str, db: Session):
    user = guest_dao.find_user_by_email(email, db)
    return 1 if user else 0


def check_token_expired(refresh_token: str):
    payload = decode_jwt_token(refresh_token)
    new_access_token = create_jwt_access_token(payload.get("login_id"), payload.get("user_id"))
    new_refresh_token = create_jwt_refresh_token(payload.get("login_id"), payload.get("user_id"))
    return UserTokenDto(access_token=new_access_token, refresh_token=new_refresh_token, token_type="bearer")


def login(user_login_dto: UserLoginDto, db: Session):
    db_user = guest_dao.find_user_by_login_id(user_login_dto.login_id, db)
    if db_user is None or db_user.hashing_password != hash_function(user_login_dto.password):
        raise HTTPException(status_code=EXCEPTION_TYPE.ERROR_422.value["code"], detail=EXCEPTION_TYPE.ERROR_422.value["message"])

    access_token = create_jwt_access_token(db_user.login_id, db_user.user_id)
    refresh_token = create_jwt_refresh_token(db_user.login_id, db_user.user_id)
    return UserTokenDto(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


def sign_up(user: UserSignUpDto, db: Session):
    email = user.email
    password = hash_function(user.password)
    print(f"email: {email}, password: {password}")
    new_user = User(
        user_name           = user.user_name,
        nickname            = user.nickname,
        email               = email,
        login_id            = email,
        hashing_password    = password,  # 비밀번호 해싱 함수를 사용하여 저장한다고 가정
    )
    user = database_util.domain_save(new_user, db)
    return user


def save_sign_up_history(user_id: int, sign_up_type_code: str, db: Session):
    sign_up_history = SignUpHistory(
        user_id             = user_id,
        sign_up_type_code   = sign_up_type_code,
        created_datetime    = get_seoul_datetime_format()
    )
    return database_util.domain_save(sign_up_history, db)


def save_verification_code(email: str, code: str, db: Session):
    email_verification_request = EmailVerificationRequest(
        email   = email,
        code    = code
    )
    return database_util.domain_save(email_verification_request, db)


def reset_password(user_id: int, db: Session):
    user = guest_dao.find_user_by_user_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=EXCEPTION_TYPE.ERROR_505.value["code"], detail=EXCEPTION_TYPE.ERROR_505.value["message"])
    random_password = generate_random_string(8)
    user.hashing_password = hash_function(random_password)
    user.update_datetime = get_seoul_datetime_format()
    user = database_util.domain_save(user, db)
    return {"email": user.email, "random_password": random_password}


def verify_code(email: str, code: int, db: Session):
    verification_code_db = guest_dao.find_verification_code(email, db)
    if verification_code_db and verification_code_db.code == str(code):
        verification_code_db.is_use = '0'
        database_util.domain_save(verification_code_db, db)
        return True
    else:
        raise HTTPException(status_code=EXCEPTION_TYPE.ERROR_401.value["code"], detail=EXCEPTION_TYPE.ERROR_401.value["message"])
