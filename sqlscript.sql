create database twitter;

use twitter;

create table tweets (
 id int auto_increment primary key,
 user text(128) not null,
 tweet_content text(1024) not null,
 timestamp timestamp default now()
);