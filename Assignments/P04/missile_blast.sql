--
-- PostgreSQL database dump
--

-- Dumped from database version 14.5 (Homebrew)
-- Dumped by pg_dump version 14.4

-- Started on 2022-10-11 19:13:11 CDT

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
-- TOC entry 240 (class 1259 OID 19893)
-- Name: missile_blast; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.missile_blast (
    cat numeric NOT NULL,
    blast_radius numeric
);


ALTER TABLE public.missile_blast OWNER TO postgres;

--
-- TOC entry 4533 (class 0 OID 19893)
-- Dependencies: 240
-- Data for Name: missile_blast; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.missile_blast (cat, blast_radius) VALUES (1, 100.0000000000000000);
INSERT INTO public.missile_blast (cat, blast_radius) VALUES (2, 150.0000000000000000);
INSERT INTO public.missile_blast (cat, blast_radius) VALUES (3, 200.0000000000000000);
INSERT INTO public.missile_blast (cat, blast_radius) VALUES (4, 250.0000000000000000);
INSERT INTO public.missile_blast (cat, blast_radius) VALUES (5, 300.0000000000000000);
INSERT INTO public.missile_blast (cat, blast_radius) VALUES (6, 350.0000000000000000);
INSERT INTO public.missile_blast (cat, blast_radius) VALUES (7, 400.0000000000000000);
INSERT INTO public.missile_blast (cat, blast_radius) VALUES (8, 450.0000000000000000);
INSERT INTO public.missile_blast (cat, blast_radius) VALUES (9, 500.0000000000000000);


--
-- TOC entry 4388 (class 2606 OID 19899)
-- Name: missile_blast missile_blast_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.missile_blast
    ADD CONSTRAINT missile_blast_pkey PRIMARY KEY (cat);


-- Completed on 2022-10-11 19:13:11 CDT

--
-- PostgreSQL database dump complete
--

