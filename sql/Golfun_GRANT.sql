create user developer@'%' identified by '1234';
create database sebatun default character set utf8;
grant all privileges on sebatun.* to developer@'%';