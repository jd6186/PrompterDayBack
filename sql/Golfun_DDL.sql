
create table `tb_participant`
(
    `participant_id`   bigint        not null auto_increment comment '참여자 고유번호',
    `user_id`          bigint        not null comment '유저고유번호(null인 경우 비회원)',
    `is_player`        varchar(1)    null     default '1' comment '0: 갤러리, 1: 플레이어',
    `player_nickname`  varchar(100)  not null comment '유저 닉네임이 디폴트(게임방에서 사용할 닉네임으로 수정 가능)',
    `memo`             varchar(1000) null comment '유저 작성 메모',
    `field_type_code`  int           not null comment '1: 필드, 2: 스크린',
    `created_datetime` datetime      not null default current_timestamp() comment '최초참여일시',
    `leave_datetime`   datetime      null     default current_timestamp() comment '게임에서 이탈한 일시(종료 시 종료 일시)',
    primary key (`participant_id`)
);

create table `tb_user`
(
    `user_id`          bigint        not null auto_increment comment '유저고유번호',
    `user_name`        varchar(1000) not null comment '유저명(외국인 고려)',
    `nickname`         varchar(100)  not null comment '닉네임',
#     `phone`            varchar(20)   not null unique comment '휴대폰번호(외국인고려)',
#     `nation_code`      varchar(10)   not null comment '나라코드',
#     `gender_code`      varchar(1)    not null comment '0: 여자, 1: 남자',
#     `birth_day`        varchar(8)    not null comment '생년월일',
    `email`            varchar(100)  not null unique comment '이메일',
    `login_id`         varchar(100)  not null unique comment '로그인 아이디',
    `hashing_password` varchar(1000)  not null comment '해싱된 로그인 패스워드(sns 가입 시 필요 없음)',
    `created_datetime` datetime      not null default current_timestamp() comment '생성일시',
    `update_datetime`  datetime      not null default current_timestamp() comment '수정일시',
    `status_code`      varchar(1)    not null default '1' comment '0: 탈퇴회원, 1: 일반회원',
    primary key (`user_id`)
);

create table `tb_friend`
(
    `friend_id`          bigint   not null comment '친구 목록 고유번호',
    `user_id`          bigint   not null comment '기준유저',
    `friend_user_id`   bigint   not null comment '친구유저-한쪽에서만 수락해도 양쪽으로 쌓이는 로직 구현',
    `created_datetime` datetime not null default current_timestamp() comment '생성일시',
    primary key (`friend_id`)
);

create table `tb_friend_invitation_history`
(
    `friend_invitation_history_id` bigint   not null auto_increment comment '친구초대이력 고유번호',
    `user_id`                      bigint   not null comment '친구 요청 유저고유번호',
    `friend_user_id`               bigint   not null comment '친구요청받은유저고유번호',
    `created_datetime`             datetime not null default current_timestamp() comment '생성일시',
    `agree_datetime`               datetime not null comment '초대수락일시',
    primary key (`friend_invitation_history_id`)
);

create table `tb_email_verification_request`
(
    `verification_code_id` bigint       not null auto_increment comment '이메일 인증 요청 발송 고유번호',
    `email`                varchar(100) null comment '이메일',
    `code`                 varchar(100) null comment '발송된 코드번호',
    `created_datetime`     datetime     not null default current_timestamp() comment '발송일시',
    `is_use`           varchar(1)    not null default '1' comment '0: 사용불가, 1:사용가능',
    primary key (`verification_code_id`)
);

create table `tb_sign_up_history`
(
    `sign_up_history_id` bigint       not null auto_increment comment '회원가입이력 고유번호',
    `user_id`            bigint       not null comment '유저고유번호',
    `sign_up_type_code`  varchar(1)   not null comment '1:일반회원가입, 2:구글, 3:페이스북, 4:카카오톡, 5:트위터',
    `sns_user_id`        varchar(100) not null default '0' comment 'sns에서 발급된 유저 식별자',
    `created_datetime`   datetime     not null default current_timestamp() comment '가입일시',
    primary key (`sign_up_history_id`)
);



alter table `tb_participant`
    add constraint `fk_tb_user_to_tb_participant_1` foreign key (
                                                                 `user_id`
        )
        references `tb_user` (
                              `user_id`
            );

alter table `tb_friend`
    add constraint `fk_tb_user_to_tb_friend_1` foreign key (
                                                            `user_id`
        )
        references `tb_user` (
                              `user_id`
            );

alter table `tb_friend`
    add constraint `fk_tb_user_to_tb_friend_2` foreign key (
                                                            `friend_user_id`
        )
        references `tb_user` (
                              `user_id`
            );

alter table `tb_friend_invitation_history`
    add constraint `fk_tb_user_to_tb_friend_invitation_history_1` foreign key (
                                                                               `user_id`
        )
        references `tb_user` (
                              `user_id`
            );

alter table `tb_friend_invitation_history`
    add constraint `fk_tb_user_to_tb_friend_invitation_history_2` foreign key (
                                                                               `friend_user_id`
        )
        references `tb_user` (
                              `user_id`
            );

alter table `tb_sign_up_history`
    add constraint `fk_tb_user_to_tb_sign_up_history_1` foreign key (
                                                                     `user_id`
        )
        references `tb_user` (
                              `user_id`
            );
