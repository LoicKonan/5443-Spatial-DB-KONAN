-- Table: public.battery

-- DROP TABLE IF EXISTS public.battery;

CREATE TABLE IF NOT EXISTS public.battery
(
    id integer NOT NULL,
    geom geometry(Point,4326),
    CONSTRAINT battery_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.battery
    OWNER to postgres;