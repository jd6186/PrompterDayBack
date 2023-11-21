from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from random import randint
from fastapi.security import HTTPBearer

from src.api.user.response_dto import UserDto
from src.api.guest.code import SignUpType
from src.api.guest.request_dto import UserLoginDto, UserSignUpDto, VerificationCodeDto, VerificationUserCodeDto
from src.api.guest.response_dto import UserTokenDto
from src.api.guest import service as guest_service
from src.core.database.database import get_db
from src.core.dto.response_dto import ResponseDTO
from src.core.util import email_util
from src.core.util.email_util import send_temp_password_email

router = APIRouter(
    tags=["Guest Manage"],
)
token_auth_scheme = HTTPBearer()


# 회원가입 관련
@router.post("/sign-up", response_model=UserDto, summary="회원가입", description="회원가입")
async def sign_up(user_sign_up: UserSignUpDto, db: Session = Depends(get_db)):
    print(f"sign_up start: {user_sign_up}")
    # TODO - 이메일 인증 기능 추가 필요 시 주석 해제
    # guest_service.verify_code(user_sign_up.email, user_sign_up.verification_code, db)
    response = guest_service.sign_up(user_sign_up, db).to_dto(UserDto)
    # 회원가입 이력 저장
    if response is not None:
        guest_service.save_sign_up_history(response["user_id"], SignUpType.NORMAL.value, db)
    db.commit()
    response["hashing_password"] = None
    return ResponseDTO().of(response)


@router.get("/check-nickname", response_model=str, summary="닉네임 중복 확인", description="닉네임 중복 확인")
async def check_duplicate_login_id(nickname: str, db: Session = Depends(get_db)):
    print(f"check_duplicate_login_id start: {nickname}")
    if guest_service.check_duplicate_nickname(nickname, db) == 1:
        response = "이미 사용중인 닉네임입니다."
    else:
        response = "사용 가능한 닉네임입니다."
    return ResponseDTO().of(response)


@router.get("/check-email", response_model=str, summary="이메일 중복 확인", description="이메일 중복 확인")
async def check_duplicate_email(email: str, db: Session = Depends(get_db)):
    print(f"check_duplicate_email start: {email}")
    if guest_service.check_duplicate_email(email, db) == 1:
        response = "이미 가입한 이메일입니다. 다시 확인해주세요."
    else:
        response = "사용 가능한 이메일입니다."
    return ResponseDTO().of(response)


# 아이디/비밀번호 찾기 관련
@router.post("/get-login-id", response_model=str, summary="로그인 아이디 찾기", description="본인 확인을 위한 코드 확인 후 맞다면 로그인 아이디 정보 전달", deprecated=True)
def get_login_id(verification_code: VerificationCodeDto, db: Session = Depends(get_db)):
    print(f"get_login_id start: {verification_code}")
    guest_service.verify_code(verification_code.email, verification_code.code, db)
    response = guest_service.get_user_login_id_by_email(verification_code.email, db)
    db.commit()
    return ResponseDTO().of(response)


@router.put('/reset-password', response_model=str, summary="비밀번호 찾기 시 패스워드 초기화", description="비밀번호 찾기 시 패스워드 초기화")
def reset_password(verification_user_code: VerificationUserCodeDto, db: Session = Depends(get_db)):
    print(f"reset_password start: {verification_user_code}")
    user = guest_service.get_user_detail_by_email(verification_user_code.email, db)
    user_data_dict = guest_service.reset_password(user.user_id, db)
    send_temp_password_email(user_data_dict['email'], user_data_dict['random_password'])
    db.commit()

    response = "메일이 발송되었습니다. 계정과 연결된 메일을 확인해주세요."
    response = user_data_dict['random_password']
    # TODO - 추후 메시지가 리턴되도록 수정 필요
    return ResponseDTO().of(response)


@router.post("/send-verification-email", response_model=str, summary="인증 코드 발송", description="인증 코드 발송(회원가입, 아이디찾기, 패스워드 초기화)", deprecated=True)
def send_verification_email(email: str, db: Session = Depends(get_db)):
    print(f"send_verification_email start: {email}")
    code = randint(100000, 999999)
    guest_service.save_verification_code(email, str(code), db)
    email_util.send_verification_email(email, code)
    response = "메일이 발송되었습니다. 메일을 확인해주세요."
    db.commit()
    return ResponseDTO().of(response)


# 유저 인증 및 로그인 관련
@router.post("/login", response_model=UserTokenDto, summary="user login", description="user login")
async def login(user_login: UserLoginDto, db: Session = Depends(get_db)):
    print(f"login start: {user_login}")
    response = guest_service.login(user_login, db)
    return ResponseDTO().of(response.dict())


@router.get("/check-refresh-token", response_model=UserTokenDto, summary="RefreshToken 체크 ", description="RefreshToken 체크 후 AccessToken과 함께 재발급")
async def check_duplicate_email(refresh_token: str):
    print(f"check_duplicate_email start: {refresh_token}")
    response = guest_service.check_token_expired(refresh_token)
    return ResponseDTO().of(response.dict())

