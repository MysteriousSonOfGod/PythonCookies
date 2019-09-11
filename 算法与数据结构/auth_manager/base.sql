create user interview with SUPERUSER CREATEDB CREATEROLE INHERIT LOGIN REPLICATION password 'interview';

create database auth_manager owner interview;

create table res_users (
    id serial not null,
    is_admin boolean default false,
    login varchar(64) not null unique,
    password varchar,
	access_token varchar,
    primary key(id)
);

create table res_contents (
    id serial not null,
    contents varchar,
    user_id integer, -- references res_users,
    primary key(id)
);


insert into res_users (login, password, is_admin) VALUES ('admin', 'admin', true);
insert into res_users (login, password) VALUES ('user0', 'user0');
insert into res_users (login, password) VALUES ('user1', 'user1');

insert into res_contents (contents, user_id) values ('管理文章', 1);
insert into res_contents (contents, user_id) values ('管理文章2', 1);
insert into res_contents (contents, user_id) values ('普通文章', 2);
insert into res_contents (contents, user_id) values ('普通文章1', 3);