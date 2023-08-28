from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.api.user import dao as user_dao
from src.api.user.request_dto import UserUpdateDto, UserPasswordUpdateDto
from src.core.error.error_type_code import EXCEPTION_TYPE
from src.core.util import database_util
from src.core.util.core_util import hash_function, get_seoul_datetime_format


def get_user_detail_by_id(user_id: int, db: Session):
    user = user_dao.find_user_by_user_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=EXCEPTION_TYPE.ERROR_505.value["code"], detail=EXCEPTION_TYPE.ERROR_505.value["message"])
    return user


def get_user_detail_by_email(email: str, db: Session):
    user = user_dao.find_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=EXCEPTION_TYPE.ERROR_505.value["code"], detail=EXCEPTION_TYPE.ERROR_505.value["message"])
    return user


def update_user(user_update_dto: UserUpdateDto, db: Session):
    user = user_dao.find_user_by_user_id(user_update_dto.user_id, db)
    if user is None:
        raise HTTPException(status_code=EXCEPTION_TYPE.ERROR_505.value["code"], detail=EXCEPTION_TYPE.ERROR_505.value["message"])

    user.nickname        = user_update_dto.nickname if user_update_dto.nickname is not None else user.nickname
    user.update_datetime = get_seoul_datetime_format()
    database_util.domain_save(user, db)
    return 1 if user else 0


def update_password(user_password_update: UserPasswordUpdateDto, db: Session):
    user = user_dao.find_user_by_user_id(user_password_update.user_id, db)
    if user.hashing_password != hash_function(user_password_update.current_password):
        raise HTTPException(status_code=EXCEPTION_TYPE.ERROR_401.value["code"], detail=EXCEPTION_TYPE.ERROR_401.value["message"])
    if user is None:
        raise HTTPException(status_code=EXCEPTION_TYPE.ERROR_505.value["code"], detail=EXCEPTION_TYPE.ERROR_505.value["message"])
    user.hashing_password = hash_function(user_password_update.after_password)
    user.update_datetime = get_seoul_datetime_format()
    database_util.domain_save(user, db)
    return 1 if user else 0


def withdrawal_user(user_id: int, db: Session):
    user = user_dao.find_user_by_user_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=EXCEPTION_TYPE.ERROR_505.value["code"], detail=EXCEPTION_TYPE.ERROR_505.value["message"])
    user.status_code = 0
    user = database_util.domain_save(user, db)
    return 1 if user else 0