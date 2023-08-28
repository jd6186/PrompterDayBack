from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserDto(BaseModel):
    user_id: Optional[int]
    user_name: Optional[str]
    nickname: Optional[str]
    email: Optional[str]
    login_id: Optional[str]
    hashing_password: Optional[str]
    created_datetime: Optional[datetime]
    update_datetime: Optional[datetime]
