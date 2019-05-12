-- This file contains the definitions of the tables used in the application.

--user table
create table usr(user_id serial primary key, first_name varchar(10), last_name varchar(10), email varchar(30), phone_number varchar(10), password varchar(20), user_name varchar(16));

--chat tables
create table chat(chid serial primary key, chat_name varchar(15), user_id integer references usr(user_id));

--chat members table
create table member(chid integer references chat(chid), user_id integer references usr(user_id), primary key(chid, user_id));

--contacts table
create table contact(contacts integer references usr(user_id), contacted integer references usr(user_id), primary key(contacts, contacted));

--photo or video table
create table media(media_id serial primary key, mediaType char(5),  file varchar(200))

--messages table
create table message(message_id serial primary key, message varchar(140), time_stamp timestamp, user_id integer references usr(user_id), chid integer references chat(chid), media_id integer references media(media_id));

--reply messages table
create table isReply(original integer references message(message_id), reply integer references message(message_id), primary key(original, reply)) ;

--like or dislike table
create table react(user_id integer references usr(user_id), message_id integer references message(message_id), primary key(user_id, message_id), reaction varchar(7), time_stamp timestamp);

--hashtag table
create table hashtag(tag_id serial primary key, hashtag varchar(30));

--messsage hashtag table
create table hasHash(message_id integer references message(message_id), tag_id integer references hashtag(tag_id), primary key (message_id, tag_id));
