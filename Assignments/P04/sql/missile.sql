--
-- PostgreSQL database dump
--

-- Dumped from database version 14.5 (Homebrew)
-- Dumped by pg_dump version 14.4

-- Started on 2022-10-11 19:11:42 CDT

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
-- TOC entry 238 (class 1259 OID 19878)
-- Name: missile; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.missile (
    id numeric NOT NULL,
    name text,
    "speedCat" numeric,
    "blastCat" numeric
);


ALTER TABLE public.missile OWNER TO postgres;

--
-- TOC entry 4533 (class 0 OID 19878)
-- Dependencies: 238
-- Data for Name: missile; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.missile (id, name, "speedCat", "blastCat") VALUES (0, 'Atlas', 1, 7);
INSERT INTO public.missile (id, name, "speedCat", "blastCat") VALUES (1, 'Harpoon', 2, 8);
INSERT INTO public.missile (id, name, "speedCat", "blastCat") VALUES (2, 'Hellfire', 3, 7);
INSERT INTO public.missile (id, name, "speedCat", "blastCat") VALUES (3, 'Javelin', 4, 7);
INSERT INTO public.missile (id, name, "speedCat", "blastCat") VALUES (4, 'Minuteman', 5, 9);
INSERT INTO public.missile (id, name, "speedCat", "blastCat") VALUES (5, 'Patriot', 6, 6);
INSERT INTO public.missile (id, name, "speedCat", "blastCat") VALUES (6, 'Peacekeeper', 7, 6);
INSERT INTO public.missile (id, name, "speedCat", "blastCat") VALUES (7, 'SeaSparrow', 8, 5);
INSERT INTO public.missile (id, name, "speedCat", "blastCat") VALUES (8, 'Titan', 8, 5);
INSERT INTO public.missile (id, name, "speedCat", "blastCat") VALUES (9, 'Tomahawk', 9, 6);
INSERT INTO public.missile (id, name, "speedCat", "blastCat") VALUES (10, 'Trident', 9, 9);


--
-- TOC entry 4388 (class 2606 OID 19884)
-- Name: missile missiles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.missile
    ADD CONSTRAINT missiles_pkey PRIMARY KEY (id);


-- Completed on 2022-10-11 19:11:43 CDT

--
-- PostgreSQL database dump complete
--

