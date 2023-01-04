-- Table: public.arsenal

-- DROP TABLE IF EXISTS public.arsenal;

CREATE TABLE IF NOT EXISTS public.arsenal
(
    atlas character varying(128) COLLATE pg_catalog."default",
    harpoon character varying(128) COLLATE pg_catalog."default",
    hellfire character varying(128) COLLATE pg_catalog."default",
    javelin character varying(128) COLLATE pg_catalog."default",
    minuteman character varying(128) COLLATE pg_catalog."default",
    patriot character varying(128) COLLATE pg_catalog."default",
    peacekeeper character varying(128) COLLATE pg_catalog."default",
    seasparrow character varying(128) COLLATE pg_catalog."default",
    titan character varying(128) COLLATE pg_catalog."default",
    tomahawk character varying(128) COLLATE pg_catalog."default",
    trident character varying(128) COLLATE pg_catalog."default",
    total character varying(128) COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.arsenal
    OWNER to postgres;