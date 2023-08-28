from pydantic import BaseModel


class UserTokenDto(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

