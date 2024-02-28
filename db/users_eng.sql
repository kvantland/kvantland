SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;
set search_path to kvantland;


COPY Kvantland.Student ("student", "login", "password", "name", "score") FROM stdin;
1	zumen	$pbkdf2-sha256$29000$trZWqjXmXKtVSqn13puTkg$KS32OoYadv3oJ/Pg6u1/9MASbb/x5PamIRaAOie0jOw	\N	10
2	testovich	$pbkdf2-sha256$29000$FIJQai0F4Dwn5Px/b83Zmw$yIpK7wY89GTR7tzUD4aDV5NyOOovPsQHxiAdc0Z0UGM	\N	10
3	testerskiy	$pbkdf2-sha256$29000$b43xvtf6/5.zVkopxdh7Lw$KJPMq/0glM8ZbL8HwzaUJHU0xV6rJRHoaUDfBwFoS5E	\N	10
\.

SELECT pg_catalog.setval('Kvantland.Student_student_seq', 3, true);

insert into Kvantland.Score ("student", "tournament", "score") VALUES (1, 3, 10);
insert into Kvantland.Score ("student", "tournament", "score") VALUES (2, 3, 10);
insert into Kvantland.Score ("student", "tournament", "score") VALUES (3, 3, 10);

update Kvantland.Student set email = 'test@gmail.com', name = 'a', surname = 'a', school = 'a', clas = 'Другое', town = 'a';