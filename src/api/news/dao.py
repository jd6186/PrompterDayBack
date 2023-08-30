from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.core.database.domain import News
from src.core.util import database_util, core_util


def insert_toon(keyword: str, content: str, img_url: str, db: Session):
    new = News(
        keyword         = keyword,
        img_url         = img_url,
        content         = content,
        show_datetime   = core_util.get_news_show_datatime_format(core_util.get_seoul_time())
    )
    return database_util.domain_save(new, db)


def find_today_news_list(date: str, db: Session):
    # 오늘 날짜에 해당하는 뉴스 리스트 조회
    return db.query(News)\
        .filter(
            and_(
                News.show_datetime == core_util.get_news_show_datatime_format_by_date(date), # 검색일자에 해당하는 모든 뉴스 리턴 > 해봤자 키워드별로 5개씩 밖에 없음
                News.show_datetime <= core_util.get_seoul_time, # 당일 오전 8시 이후에 조회 가능
                News.is_use == '1'
            )
        )\
        .all()
