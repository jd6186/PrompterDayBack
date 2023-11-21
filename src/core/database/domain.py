# coding: utf-8
from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, String, text, Text
from sqlalchemy.orm import relationship
from src.core.database.database import Base


class Serializable:
    def to_dict(self):
        data = {}
        for key, value in vars(self).items():
            if key == '_sa_instance_state':
                continue
            if isinstance(value, Serializable):
                data[key] = value.to_dict()
            elif isinstance(value, list):
                data[key] = []
                for item in value:
                    if isinstance(item, Serializable):
                        data[key].append(item.to_dict())
                    else:
                        data[key].append(item)
            elif isinstance(value, datetime):
                data[key] = value.strftime('%Y-%m-%d %H:%M:%S')
            else:
                data[key] = value
        return data

    def to_dto(self, dto_cls):
        # SQLAlchemy ORM 객체를 딕셔너리로 변환
        obj = self.to_dict()
        print(f"obj : {obj}")

        # DTO 클래스의 필드 조회
        fields = dto_cls.__annotations__

        # DTO 객체 생성
        dto_obj = dto_cls()

        # SQLAlchemy ORM 객체의 속성 값을 DTO 객체에 할당
        for field in fields.keys():
            try:
                data = obj[field]
            except KeyError:
                continue
            if data is not None:
                setattr(dto_obj, field, data)

        # DTO 객체를 반환
        return dto_obj.dict()


class User(Base, Serializable):
    __tablename__ = 'tb_user'

    # phone               = Column(String(20), nullable=False, comment='휴대폰번호(외국인고려)')
    # nation_code         = Column(String(10), nullable=False, comment='나라코드')
    # gender_code         = Column(String(1), nullable=False, comment='0: 여자, 1: 남자')
    # birth_day           = Column(String(8), nullable=False, comment='생년월일')
    user_id             = Column(BigInteger, primary_key=True, comment='유저고유번호')
    user_name           = Column(String(1000), nullable=False, comment='유저명(외국인 고려)')
    nickname            = Column(String(100), nullable=False, comment='닉네임')
    email               = Column(String(100), nullable=False, comment='이메일')
    login_id            = Column(String(20), nullable=False, comment='로그인 아이디')
    status_code         = Column(String(1), nullable=False, server_default=text("'1'"), comment='0: 탈퇴회원, 1: 일반회원')
    hashing_password    = Column(String(1000), nullable=False, comment='해싱된 로그인 패스워드(SNS 가입 시 임시 패스워드 임의 발급)')
    created_datetime    = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='생성일시')
    update_datetime     = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='수정일시')


class Friend(Base, Serializable):
    __tablename__ = 'tb_friend'

    friend_id           = Column(BigInteger, primary_key=True, nullable=False, comment='친구고유번호')
    user_id             = Column(BigInteger, ForeignKey('tb_user.user_id'), primary_key=True, comment='기준유저')
    friend_user_id      = Column(BigInteger, ForeignKey('tb_friend_user.user_id'), nullable=False, index=True, comment='친구유저-한쪽에서만 수락해도 양쪽으로 쌓이는 로직 구현')
    created_datetime    = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='생성일시')

    tb_user = relationship('User')
    tb_friend_user = relationship('User')


class FriendInvitationHistory(Base, Serializable):
    __tablename__ = 'tb_friend_invitation_history'

    friend_invitation_history_id    = Column(BigInteger, primary_key=True, nullable=False, comment='친구초대이력 고유번호')
    user_id                         = Column(ForeignKey('tb_user.user_id'), nullable=False, index=True, comment='친구 요청 유저고유번호')
    friend_user_id                  = Column(ForeignKey('tb_friend_user.user_id'), nullable=False, index=True, comment='친구요청받은유저고유번호')
    created_datetime                = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='생성일시')
    agree_datetime                  = Column(DateTime, nullable=False, comment='초대수락일시')

    tb_user = relationship('User')
    tb_friend_user = relationship('User')


class SignUpHistory(Base, Serializable):
    __tablename__ = 'tb_sign_up_history'

    sign_up_history_id      = Column(BigInteger, primary_key=True, nullable=False, comment='회원가입이력 고유번호')
    user_id                 = Column(ForeignKey('tb_user.user_id'), nullable=False, index=True, comment='유저고유번호')
    sign_up_type_code       = Column(String(1), nullable=False, comment='1:일반회원가입, 2:구글, 3:페이스북, 4:카카오톡, 5:트위터')
    sns_user_id             = Column(String(100), nullable=False, server_default=text("'0'"), comment='SNS에서 발급된 유저 식별자')
    created_datetime        = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='가입일시')

    tb_user = relationship('User')


class Participant(Base, Serializable):
    __tablename__ = 'tb_participant'

    participant_id      = Column(BigInteger, primary_key=True, nullable=False, comment='참여자 고유번호')
    user_id             = Column(ForeignKey('tb_user.user_id'), nullable=False, index=True, comment='유저고유번호(NULL인 경우 비회원)')
    is_player           = Column(String(1), server_default=text("'1'"), comment='0: 갤러리, 1: 플레이어')
    memo                = Column(String(1000), nullable=True, comment='유저 작성 메모')
    player_nickname     = Column(String(100), nullable=False, comment='유저 닉네임이 디폴트(게임방에서 사용할 닉네임으로 수정 가능)')
    created_datetime    = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='최초참여일시')
    leave_datetime      = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), comment='게임에서 이탈한 일시(종료 시 종료 일시)')
    field_type_code     = Column(String(1), nullable=True, comment='1: 필드, 2: 스크린')

    tb_user = relationship('User')


class EmailVerificationRequest(Base, Serializable):
    __tablename__ = 'tb_email_verification_request'

    verification_code_id    = Column(BigInteger, primary_key=True, comment='유저고유번호')
    email                   = Column(String(100), comment='이메일')
    code                    = Column(String(100), comment='발송된 코드번호')
    created_datetime        = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='발송일시')
    is_use                  = Column(String(1), nullable=False, server_default=text("'1'"), comment='0:사용후, 1:사용전')


class News(Base, Serializable):
    __tablename__ = 'tb_news'

    news_id             = Column(BigInteger, primary_key=True, comment='뉴스고유번호')
    keyword             = Column(String(255), nullable=False, comment='키워드')
    content             = Column(Text, nullable=False, comment='키워드 설명글')
    img_url             = Column(String(100), nullable=False, comment='이미지 URL')
    show_datetime       = Column(DateTime, nullable=False, comment='노출 시작 일시')
    created_datetime    = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='저장일시')
    is_use              = Column(String(1), nullable=False, server_default=text("'1'"), comment='0:사용불가, 1:사용가능')



