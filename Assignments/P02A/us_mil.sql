-- Table: public.us_mil

-- DROP TABLE IF EXISTS public.us_mil;

CREATE TABLE IF NOT EXISTS public.us_mil
(
    gid integer NOT NULL DEFAULT nextval('tl_2021_us_mil_gid_seq'::regclass),
    ansicode character varying(8) COLLATE pg_catalog."default",
    areaid character varying(22) COLLATE pg_catalog."default",
    fullname character varying(100) COLLATE pg_catalog."default",
    mtfcc character varying(5) COLLATE pg_catalog."default",
    aland double precision,
    awater double precision,
    intptlat character varying(11) COLLATE pg_catalog."default",
    intptlon character varying(12) COLLATE pg_catalog."default",
    geom geometry(MultiPolygon),
    CONSTRAINT tl_2021_us_mil_pkey PRIMARY KEY (gid)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.us_mil
    OWNER to postgres;
-- Index: tl_2021_us_mil_geom_idx

-- DROP INDEX IF EXISTS public.tl_2021_us_mil_geom_idx;

CREATE INDEX IF NOT EXISTS tl_2021_us_mil_geom_idx
    ON public.us_mil USING gist
    (geom)
    TABLESPACE pg_default;