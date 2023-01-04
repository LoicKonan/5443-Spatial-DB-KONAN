-- Table: public.myregion

-- DROP TABLE IF EXISTS public.myregion;

CREATE TABLE IF NOT EXISTS public.myregion
(
    rid integer NOT NULL,
    geom geometry(MultiPolygon,4326),
    CONSTRAINT myregion_pkey PRIMARY KEY (rid)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.myregion
    OWNER to postgres;