insert into tb_user (user_id, user_name, nickname, email, login_id, hashing_password, created_datetime, update_datetime)
values (1, '이재민', '사슴', 'admin1', 'admin1@gmail.kr',
        '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', '2023-07-07 13:05:36',
        '2023-07-07 13:05:36');
insert into tb_user (user_id, user_name, nickname, email, login_id, hashing_password, created_datetime, update_datetime)
values (2, '정동욱', '쿼카', 'admin2', 'admin2@gmail.kr',
        '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', '2023-07-07 13:06:12',
        '2023-07-07 13:06:12');
insert into tb_user (user_id, user_name, nickname, email, login_id, hashing_password, created_datetime, update_datetime)
values (3, '테스터', '레서팬더', 'admin3', 'admin3@gmail.kr',
        '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', '2023-07-07 13:11:16',
        '2023-07-07 13:11:19');

insert into tb_sign_up_history (user_id, sign_up_type_code, sns_user_id, created_datetime)
values (1, '1', '1234567890', '2023-07-07 13:05:36');
insert into tb_sign_up_history (user_id, sign_up_type_code, sns_user_id, created_datetime)
values (2, '1', '1234567890', '2023-07-07 13:05:36');
insert into tb_sign_up_history (user_id, sign_up_type_code, sns_user_id, created_datetime)
values (3, '1', '1234567890', '2023-07-07 13:05:36');
