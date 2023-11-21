from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class NewsDto(BaseModel):
    news_id: Optional[int]
    keyword: Optional[str]
    content: Optional[str]
    img_url: Optional[str]
    show_datetime: Optional[datetime]
    created_datetime: Optional[datetime]
    is_use: Optional[str]