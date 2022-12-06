-- Table: public.missile_data

-- DROP TABLE IF EXISTS public.missile_data;

CREATE TABLE IF NOT EXISTS public.missile_data
(
    missile_id real NOT NULL,
    "current_time" time without time zone NOT NULL,
    current_loc geometry NOT NULL,
    target_id real NOT NULL,
    target_city geometry NOT NULL,
    start_time time without time zone NOT NULL,
    start_loc geometry NOT NULL,
    speed real NOT NULL,
    altitude real NOT NULL,
    drop_rate real NOT NULL,
    active boolean NOT NULL,
    CONSTRAINT missile_data_pkey PRIMARY KEY (missile_id, "current_time", current_loc)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.missile_data
    OWNER to postgres;

ALTER TABLE public.missile_data
ADD bearing real NOT NULL,
ADD missile_type text NOT NULL;

