from pydantic import BaseModel, Field
from typing import Optional


# 회원 정보 업데이트를 위한 DTO 정의
class UserUpdateDto(BaseModel):
    user_id: int
    nickname: Optional[str] = Field(max_length=100)


class UserPasswordUpdateDto(BaseModel):
    user_id: int
    current_password: str = Field(max_length=100)
    after_password: str = Field(max_length=100)
