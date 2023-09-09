--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3
-- Dumped by pg_dump version 15.3 (Debian 15.3-1.pgdg120+1)

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

--
-- Data for Name: Ученик; Type: TABLE DATA; Schema: Квантландия; Owner: postgres
--

COPY "Квантландия"."Ученик" ("ученик", "логин", "пароль", "имя", "счёт") FROM stdin;
1	zumen	$pbkdf2-sha256$29000$trZWqjXmXKtVSqn13puTkg$KS32OoYadv3oJ/Pg6u1/9MASbb/x5PamIRaAOie0jOw	\N	10
2	testovich	$pbkdf2-sha256$29000$FIJQai0F4Dwn5Px/b83Zmw$yIpK7wY89GTR7tzUD4aDV5NyOOovPsQHxiAdc0Z0UGM	\N	10
3	testerskiy	$pbkdf2-sha256$29000$b43xvtf6/5.zVkopxdh7Lw$KJPMq/0glM8ZbL8HwzaUJHU0xV6rJRHoaUDfBwFoS5E	\N	10
\.


--
-- Name: Ученик_ученик_seq; Type: SEQUENCE SET; Schema: Квантландия; Owner: postgres
--

SELECT pg_catalog.setval('"Квантландия"."Ученик_ученик_seq"', 3, true);


--
-- PostgreSQL database dump complete
--

