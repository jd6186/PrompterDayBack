import openai
import requests
from sqlalchemy.orm import Session

from src.core.util.core_util import get_secret_data
from src.api.news import dao

# openai chatGPT3.5
SECRET_DATA = get_secret_data()
openai.api_key = SECRET_DATA["OPENAI_API_KEY"]


def get_today_keywords(text: str):
    # TODO - 가능하다면 Kakao API를 이용해서 키워드 추출하기
    url = "KAKAO_KEYWORD_SEARCH_ENDPOINT"
    headers = {
        "x-api-key": "KAKAO_CLIENT_ID",
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
    }
    kakao_response = requests.post(url, headers=headers, data=data)
    if kakao_response.status_code == 200:
        result = kakao_response.json()
        if 'keywords' in result:
            result = result['keywords']
        else:
            result = {"error": "No keywords found."}
    else:
        result = {"error": f"Error occurred while calling Kakao Keyword Extraction API: {kakao_response.status_code}"}

    # TODO - KAKAO_CLIENT_ID 발급 전까지 활용할 임시 Response
    result = {
        "keywords": ["부동산 부채", "미국 신용도 하락", "DSL 규제 완화", "부채의 자산화", "기준 금리 인상"]
    }
    return result


def ask_chat_gpt(question : str):
    # TODO - 돈들어오면 주석 해제
    # chat_gpt = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": "You are a helpful assistant."},
    #         {"role": "user", "content": question},
    #     ]
    # )
    # result = {"answer": chat_gpt['choices'][0]['message']['content']}
    result = "answer"
    return result


def make_toon(chat_gpt_text: str, db: Session):
    print(f"make_toon start : {chat_gpt_text}")
    url = "url~"
    # TODO - 돈들어오면 주석 해제
    # prompt = "아래 내용을 바탕으로 4컷 만화를 제작해주세요.\n\n" + chat_gpt_text
    # response = openai.Image.create(
    #     prompt=prompt,
    #     n=1,
    #     size="1024x1024"
    # )
    # print(f"data : {response['data']}")
    #
    # url = response['data'][0]['url']
    return url


def save_news(keyword: str, content: str, img_url: str, db: Session):
    return dao.insert_toon(keyword, content, img_url, db)


def get_today_news_list(date: str, db: Session):
    return dao.find_today_news_list(date, db)