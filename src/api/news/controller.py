from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from src.api.news import service
from src.api.news.code import NewsType
from src.core.database.database import get_db
from src.core.dto.response_dto import ResponseDTO

router = APIRouter(
    tags=["New Manage"],
)
token_auth_scheme = HTTPBearer()


@router.post("/search_keywords", summary="오늘의 키워드 검색 테스트용 API", description="오늘의 키워드 검색 테스트용 API")
async def kakao_extract_keywords(text: str):
    response = service.get_today_keywords(text)
    return ResponseDTO().of(response)


@router.post("/ask-gpt", summary="GPT3.5에 질문 테스트용 API", description="GPT3.5에 질문하기", deprecated=True)
async def ask_gpt(question: str):
    response = service.ask_chat_gpt(question)
    return ResponseDTO().of(response)


@router.get("/today-batch", summary="오늘의 키워드를 산정하고 이를 DALL·E 2를 활용해 웹툰을 만들어두는 배치", description="현재는 경제관련 용어만 질문")
async def make_today_data_batch(db: Session = Depends(get_db)):
    for name, data in NewsType.__members__.items():
        print(f"make_today_data_batch > name : {name}, data.value : {data.value}")
        # 질문에 맞는 키워드 추출
        today_keywords = service.get_today_keywords(data.value["name"])
        print("today_5_keyword : " + today_keywords)
        for keyword in today_keywords:
            # 키워드 용어 설명을 ChatGPT에 문의
            content = service.ask_chat_gpt(keyword)

            # 답변 기반으로 4컷 만화 제작
            url = service.make_toon(content, db)

            # 뉴스 기록 DB 저장
            service.save_news(keyword, content, url, db)
    db.commit()
    return ResponseDTO().of("success")


@router.get("/today-news", summary="오늘의 키워드를 산정하고 이를 DALL·E 2를 활용해 웹툰을 만들어두는 배치", description="현재는 경제관련 용어만 질문")
async def get_today_news(date: str, db: Session = Depends(get_db)):
    response = service.get_today_news_list(date, db)
    return ResponseDTO().of(response)