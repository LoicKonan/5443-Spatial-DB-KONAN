-- Table: public.airports

-- DROP TABLE IF EXISTS public.airports;

CREATE TABLE IF NOT EXISTS public.airports
(
    id numeric NOT NULL,
    name text COLLATE pg_catalog."default",
    city text COLLATE pg_catalog."default",
    country text COLLATE pg_catalog."default",
    three_code text COLLATE pg_catalog."default",
    four_code text COLLATE pg_catalog."default",
    lat numeric,
    lon numeric,
    elevation numeric,
    gmt numeric,
    tz_short text COLLATE pg_catalog."default",
    time_zone text COLLATE pg_catalog."default",
    type text COLLATE pg_catalog."default",
    geom geometry(Point,4326),
    CONSTRAINT airports_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.airports
    OWNER to postgres;