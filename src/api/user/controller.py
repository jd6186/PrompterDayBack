from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, OAuth2PasswordBearer

from src.api.user.request_dto import UserUpdateDto, UserPasswordUpdateDto
from src.api.user.response_dto import UserDto
from src.api.user import service as user_service
from src.core.database.database import get_db
from src.core.dto.response_dto import ResponseDTO

router = APIRouter(
    tags=["User Manage"],
)
token_auth_scheme = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/detail", response_model=UserDto, summary="user 신상 정보 조회", description="user 신상 정보 조회")
async def get_user(user_email: str, db: Session = Depends(get_db)):
    print(f"get_user start: {user_email}")
    response = user_service.get_user_detail_by_email(user_email, db).to_dto(UserDto)
    response["hashing_password"] = None
    return ResponseDTO().of(response)


@router.put('/update', response_model=int, summary="회원 정보 수정", description="현재는 닉네임만 변경 가능(1: 수정성공, 0: 수정실패)")
def update_user(user_update_dto: UserUpdateDto, db: Session = Depends(get_db)):
    print(f"update_user start: {user_update_dto}")
    response = user_service.update_user(user_update_dto, db)
    db.commit()
    return ResponseDTO().of(response)


@router.put('/update-password', response_model=int, summary="패스워드 회원 직접 변경", description="패스워드 회원 직접 변경(1: 수정성공, 0: 수정실패)")
def update_password(user_password_update: UserPasswordUpdateDto, db: Session = Depends(get_db)):
    print(f"update_password start: {user_password_update}")
    response = user_service.update_password(user_password_update, db)
    db.commit()
    return ResponseDTO().of(response)


@router.delete('/withdrawal', response_model=int, summary="회원탈퇴", description="회원탈퇴(1: 탈퇴성공, 0: 탈퇴실패)")
def withdrawal_user(user_id: int, db: Session = Depends(get_db)):
    print(f"withdrawal_user start: {user_id}")
    response = user_service.withdrawal_user(user_id, db)
    db.commit()
    return ResponseDTO().of(response)