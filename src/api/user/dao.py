from sqlalchemy.orm import Session

from src.core.database.domain import User, EmailVerificationRequest


def find_user_by_login_id(login_id: str, db: Session):
    return db.query(User).filter(User.login_id == login_id, User.status_code == '1').first()


def find_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email, User.status_code == '1').first()


def find_user_by_user_id(user_id: int, db: Session):
    return db.query(User) \
        .filter(
        User.user_id == user_id,
        User.status_code == '1'
    ) \
        .first()


def find_verification_code(email: str, db: Session):
    return db.query(EmailVerificationRequest) \
        .filter(EmailVerificationRequest.email == email, EmailVerificationRequest.is_use == '1') \
        .order_by(EmailVerificationRequest.created_datetime.desc()) \
        .first()


def find_user_login_id_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email, User.status_code == '1').first().login_id
