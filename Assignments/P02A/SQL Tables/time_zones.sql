-- Table: public.time_zones

-- DROP TABLE IF EXISTS public.time_zones;

CREATE TABLE IF NOT EXISTS public.time_zones
(
    gid integer NOT NULL DEFAULT nextval('ne_10m_time_zones_gid_seq'::regclass),
    objectid integer,
    scalerank smallint,
    featurecla character varying(50) COLLATE pg_catalog."default",
    name character varying(50) COLLATE pg_catalog."default",
    map_color6 smallint,
    map_color8 smallint,
    note character varying(250) COLLATE pg_catalog."default",
    zone double precision,
    utc_format character varying(50) COLLATE pg_catalog."default",
    time_zone character varying(254) COLLATE pg_catalog."default",
    iso_8601 character varying(254) COLLATE pg_catalog."default",
    places character varying(254) COLLATE pg_catalog."default",
    dst_places character varying(254) COLLATE pg_catalog."default",
    tz_name1st character varying(100) COLLATE pg_catalog."default",
    tz_namesum smallint,
    geom geometry(MultiPolygon),
    CONSTRAINT ne_10m_time_zones_pkey PRIMARY KEY (gid)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.time_zones
    OWNER to postgres;
-- Index: ne_10m_time_zones_geom_idx

-- DROP INDEX IF EXISTS public.ne_10m_time_zones_geom_idx;

CREATE INDEX IF NOT EXISTS ne_10m_time_zones_geom_idx
    ON public.time_zones USING gist
    (geom)
    TABLESPACE pg_default;