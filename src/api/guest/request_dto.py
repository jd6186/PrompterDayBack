from pydantic import BaseModel, Field


class UserLoginDto(BaseModel):
    login_id: str = Field(max_length=100)
    password: str = Field(max_length=100)


class UserSignUpDto(BaseModel):
    user_name: str = Field(max_length=1000)
    nickname: str = Field(max_length=100)
    email: str = Field(max_length=100)
    password: str = Field(max_length=1000)
    # TODO - 이메일 인증 필요 시 주석 해제
    # verification_code: int = Field(le=1000000)


class VerificationCodeDto(BaseModel):
    email: str = Field(max_length=100)
    code: int = Field(le=1000000)


class VerificationUserCodeDto(BaseModel):
    email: str = Field(max_length=100)

