create user developer@'%' identified by '1234';
create database sebatoon default character set utf8;
grant all privileges on sebatoon.* to developer@'%';