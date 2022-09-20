-- Table: public.us_state

-- DROP TABLE IF EXISTS public.us_state;

CREATE TABLE IF NOT EXISTS public.us_state
(
    gid integer NOT NULL DEFAULT nextval('tl_2021_us_state_gid_seq'::regclass),
    region character varying(2) COLLATE pg_catalog."default",
    division character varying(2) COLLATE pg_catalog."default",
    statefp character varying(2) COLLATE pg_catalog."default",
    statens character varying(8) COLLATE pg_catalog."default",
    geoid character varying(2) COLLATE pg_catalog."default",
    stusps character varying(2) COLLATE pg_catalog."default",
    name character varying(100) COLLATE pg_catalog."default",
    lsad character varying(2) COLLATE pg_catalog."default",
    mtfcc character varying(5) COLLATE pg_catalog."default",
    funcstat character varying(1) COLLATE pg_catalog."default",
    aland double precision,
    awater double precision,
    intptlat character varying(11) COLLATE pg_catalog."default",
    intptlon character varying(12) COLLATE pg_catalog."default",
    geom geometry(MultiPolygon),
    CONSTRAINT tl_2021_us_state_pkey PRIMARY KEY (gid)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.us_state
    OWNER to postgres;
-- Index: tl_2021_us_state_geom_idx

-- DROP INDEX IF EXISTS public.tl_2021_us_state_geom_idx;

CREATE INDEX IF NOT EXISTS tl_2021_us_state_geom_idx
    ON public.us_state USING gist
    (geom)
    TABLESPACE pg_default;