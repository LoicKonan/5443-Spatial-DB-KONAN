-- Table: public.defender_stats

-- DROP TABLE IF EXISTS public.defender_stats;

CREATE TABLE IF NOT EXISTS public.defender_stats
(
    team_id numeric NOT NULL,
    missile_targeted_at_region numeric,
    missiles_hit_by_team numeric
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.defender_stats
    OWNER to postgres;