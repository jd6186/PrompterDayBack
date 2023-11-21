import json
import re
import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from src.api.news.response_dto import NewsDto
from src.api.news import dao
from src.core.util import gpt_util


def get_today_keywords(text: str):
    # TODO - 가능하다면 Kakao API를 이용해서 키워드 추출하기
    # url = "KAKAO_KEYWORD_SEARCH_ENDPOINT"
    # headers = {
    #     "x-api-key": "KAKAO_CLIENT_ID",
    #     "Content-Type": "application/json"
    # }
    # data = {
    #     "text": text,
    # }
    # kakao_response = requests.post(url, headers=headers, data=data)
    # if kakao_response.status_code == 200:
    #     result = kakao_response.json()
    #     if 'keywords' in result:
    #         result = result['keywords']
    #     else:
    #         result = {"error": "No keywords found."}
    # else:
    #     result = {"error": f"Error occurred while calling Kakao Keyword Extraction API: {kakao_response.status_code}"}

    # TODO - KAKAO_CLIENT_ID 발급 전까지 활용할 임시 Response
    result = ["부동산 부채", "미국 신용도 하락", "DSL 규제 완화", "부채의 자산화", "기준 금리 인상"]
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
    db_list = dao.find_today_news_list(date, db)
    return [news.to_dto(NewsDto) for news in db_list]


def get_crawl_news_html(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        tag_line_list = str(soup).split(">")
        count = 0
        for tag_line in tag_line_list:
            if "window.Fusion=window.Fusion||{};" in tag_line:
                text = tag_line.split('<')[0]
                # 영어 및 특수문자 제거
                clean_text = re.sub('[a-zA-Z0-9]', '', text)
                clean_text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\{\}\[\]\<\>`\'…》]', '', clean_text)

                print(f"clean_text : {clean_text}")
                # 공백을 기준으로 분리하여 배열로 변환
                keyword_select_separator = '다음 글 내 한글 중 가장 중요해보이는 키워드 10가지를 나열해주세요. 이 때 중요도 1위부터 10위를 배열로 표현해주세요.\n배열은 [{"1위": ""}, {"2위": ""}, ...] 같은 형식입니다.\n\n\n' + clean_text
                # keyword_text = gpt_util.ask_chat_gpt(keyword_select_separator)
                keyword_text = '12313212312 [{"1위": "금리 인상"}, {"2위": "예금 이자율"}, {"3위": "대출 상환 연체율"}, {"4위": "대형 저축은행"}, {"5위": "손실"}, {"6위": "실적 방어"}, {"7위": "수익원"}, {"8위": "유가증권 투자"}, {"9위": "중·소형 저축은행"}, {"10위": "경제 침체"}]'
                start_index = keyword_text.index('[')
                end_index = keyword_text.index(']')
                keyword_text = keyword_text[start_index:end_index+1]
                print(f"keyword_text : {keyword_text}")
                result_list = json.loads(keyword_text)
                print(f"result_list : {type(result_list)},{result_list}")
                return {"keywords": result_list}
        return {"keywords": "없음"}
    else:
        return {"keywords": "Failed to get the webpage"}