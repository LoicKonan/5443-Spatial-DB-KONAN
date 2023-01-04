-- Table: public.speed

-- DROP TABLE IF EXISTS public.speed;

CREATE TABLE IF NOT EXISTS public.speed
(
    id integer NOT NULL DEFAULT nextval('speed_id_seq'::regclass),
    missile_id integer,
    latitude double precision,
    longitude double precision,
    bearing double precision,
    altitude double precision,
    time1 double precision,
    altitude2 double precision,
    time2 double precision,
    drop_rate double precision,
    missile_type text COLLATE pg_catalog."default",
    speed double precision,
    CONSTRAINT speed_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.speed
    OWNER to postgres;