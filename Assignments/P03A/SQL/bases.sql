-- Table: public.US_Bases

-- DROP TABLE IF EXISTS public."US_Bases";

CREATE TABLE IF NOT EXISTS public."US_Bases"
(
    "Bases_id" numeric NOT NULL,
    gid numeric,
    health numeric,
    "numbMissiles" numeric,
    area numeric,
    center geometry[],
    CONSTRAINT "US_Bases_pkey" PRIMARY KEY ("Bases_id")
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."US_Bases"
    OWNER to postgres;