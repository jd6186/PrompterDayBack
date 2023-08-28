from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

from src.core.util.core_util import get_secret_data

SECRET_DATA = get_secret_data()
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{SECRET_DATA['username']}:{SECRET_DATA['password']}@{SECRET_DATA['host']}:3306/{SECRET_DATA['db_name']}"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 쿼리 로깅 작업
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


# Session Local 조회
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()