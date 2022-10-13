--
-- PostgreSQL database dump
--

-- Dumped from database version 14.5 (Homebrew)
-- Dumped by pg_dump version 14.4

-- Started on 2022-10-11 19:13:46 CDT

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 239 (class 1259 OID 19885)
-- Name: missile_speed; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.missile_speed (
    category numeric NOT NULL,
    ms numeric,
    mph numeric
);


ALTER TABLE public.missile_speed OWNER TO postgres;

--
-- TOC entry 4533 (class 0 OID 19885)
-- Dependencies: 239
-- Data for Name: missile_speed; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.missile_speed (category, ms, mph) VALUES (1, 111, 248.307);
INSERT INTO public.missile_speed (category, ms, mph) VALUES (2, 222, 496.614);
INSERT INTO public.missile_speed (category, ms, mph) VALUES (3, 333, 744.921);
INSERT INTO public.missile_speed (category, ms, mph) VALUES (4, 444, 993.228);
INSERT INTO public.missile_speed (category, ms, mph) VALUES (5, 555, 1241.535);
INSERT INTO public.missile_speed (category, ms, mph) VALUES (6, 666, 1489.842);
INSERT INTO public.missile_speed (category, ms, mph) VALUES (7, 777, 1738.149);
INSERT INTO public.missile_speed (category, ms, mph) VALUES (8, 888, 1986.456);
INSERT INTO public.missile_speed (category, ms, mph) VALUES (9, 999, 2234.763);


--
-- TOC entry 4388 (class 2606 OID 19891)
-- Name: missile_speed missile_speed_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.missile_speed
    ADD CONSTRAINT missile_speed_pkey PRIMARY KEY (category);


-- Completed on 2022-10-11 19:13:46 CDT

--
-- PostgreSQL database dump complete
--

