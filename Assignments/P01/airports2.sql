-- Table: public.airports2

-- DROP TABLE IF EXISTS public.airports2;

CREATE TABLE IF NOT EXISTS public.airports2
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
    location geometry(Point,4326),
    CONSTRAINT airports2_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.airports2
    OWNER to postgres;
-- Index: airport_name

-- DROP INDEX IF EXISTS public.airport_name;

CREATE INDEX IF NOT EXISTS airport_name
    ON public.airports2 USING btree
    (name COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: city_name

-- DROP INDEX IF EXISTS public.city_name;

CREATE INDEX IF NOT EXISTS city_name
    ON public.airports2 USING btree
    (city COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: country_name

-- DROP INDEX IF EXISTS public.country_name;

CREATE INDEX IF NOT EXISTS country_name
    ON public.airports2 USING btree
    (country COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: index_id

-- DROP INDEX IF EXISTS public.index_id;

CREATE INDEX IF NOT EXISTS index_id
    ON public.airports2 USING btree
    (id ASC NULLS LAST)
    TABLESPACE pg_default;