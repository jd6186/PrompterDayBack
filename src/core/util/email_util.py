import os
import smtplib
from email.mime.text import MIMEText

from src.core.util.core_util import get_secret_data

SECRET_DATA = get_secret_data()
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SMTP_HOST = os.environ.get("SMTP_HOST")
SENDER_EMAIL_PASSWORD = SECRET_DATA["SENDER_EMAIL_PASSWORD"]
print(f"SENDER_EMAIL: {SENDER_EMAIL}, SMTP_HOST: {SMTP_HOST}, SENDER_EMAIL_PASSWORD: {SENDER_EMAIL_PASSWORD}")


def send_verification_email(email: str, code: int):
    subject = "[세바툰]인증 코드 정보를 알려드립니다."
    body_text = f"인증 코드 : {code}."
    return send_email(email, subject, body_text)


def send_temp_password_email(email: str, password: str):
    subject = "[세바툰]임시 비밀번호 발급입니다."
    body_text = f"임시 비밀번호 : {password}."
    return send_email(email, subject, body_text)


def send_email(receiver: str, subject: str, body_text: str):
    smtp_host = SMTP_HOST
    smtp_port = 587  # SMTP 포트 번호

    # 이메일 구성 요소 설정
    msg = MIMEText(body_text)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver

    try:
        # SMTP 서버에 연결하여 이메일 전송
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_EMAIL_PASSWORD)  # SMTP 인증 정보 입력 (계정 정보)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"이메일 발송에 실패했습니다. : {e}")
        return False
