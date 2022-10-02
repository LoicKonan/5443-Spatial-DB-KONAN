-- Table: public.MissilesPaths

-- DROP TABLE IF EXISTS public."MissilesPaths";

CREATE TABLE IF NOT EXISTS public."MissilesPaths"
(
    "missileID" numeric NOT NULL,
    start geometry[],
    speed numeric,
    angle numeric,
    altitude numeric,
    CONSTRAINT "MissilesPaths_pkey" PRIMARY KEY ("missileID")
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."MissilesPaths"
    OWNER to postgres;