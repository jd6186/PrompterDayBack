import string
from datetime import datetime, timedelta, timezone
import hashlib
import random
import os
import json
from dotenv import load_dotenv, find_dotenv


def get_seoul_time():
    return datetime.now(timezone(timedelta(hours=9)))


def get_seoul_datetime_format():
    return "{:%Y-%m-%d %H:%M:%S}".format(get_seoul_time())


def hash_function(password: str) -> str:
    # 비밀번호를 바이트 형식으로 변환
    password_bytes = password.encode()

    # SHA-256 해시 생성 및 업데이트
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password_bytes)

    # 해시된 비밀번호를 16진수 형식의 문자열로 반환
    return sha256_hash.hexdigest()


def generate_random_string(length: int) -> str:
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def get_secret_data():
    env = os.environ.get('ENV')
    dotenv_path = "env/.env.local"
    if env:
        dotenv_path = 'env/.env.' + str(env)
    load_dotenv(find_dotenv(dotenv_path))
    secret_data = os.environ.get('SECRET_DATA')
    if secret_data:
        return json.loads(secret_data)
