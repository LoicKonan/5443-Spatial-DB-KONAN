-- Table: public.us_rails

-- DROP TABLE IF EXISTS public.us_rails;

CREATE TABLE IF NOT EXISTS public.us_rails
(
    gid integer NOT NULL DEFAULT nextval('tl_2019_us_rails_gid_seq'::regclass),
    linearid character varying(22) COLLATE pg_catalog."default",
    fullname character varying(100) COLLATE pg_catalog."default",
    mtfcc character varying(5) COLLATE pg_catalog."default",
    geom geometry(MultiLineString),
    CONSTRAINT tl_2019_us_rails_pkey PRIMARY KEY (gid)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.us_rails
    OWNER to postgres;
-- Index: tl_2019_us_rails_geom_idx

-- DROP INDEX IF EXISTS public.tl_2019_us_rails_geom_idx;

CREATE INDEX IF NOT EXISTS tl_2019_us_rails_geom_idx
    ON public.us_rails USING gist
    (geom)
    TABLESPACE pg_default;