-- Table: public.spatial_ref_sys

-- DROP TABLE IF EXISTS public.spatial_ref_sys;

CREATE TABLE IF NOT EXISTS public.spatial_ref_sys
(
    srid integer NOT NULL,
    auth_name character varying(256) COLLATE pg_catalog."default",
    auth_srid integer,
    srtext character varying(2048) COLLATE pg_catalog."default",
    proj4text character varying(2048) COLLATE pg_catalog."default",
    CONSTRAINT spatial_ref_sys_pkey PRIMARY KEY (srid),
    CONSTRAINT spatial_ref_sys_srid_check CHECK (srid > 0 AND srid <= 998999)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.spatial_ref_sys
    OWNER to postgres;

REVOKE ALL ON TABLE public.spatial_ref_sys FROM PUBLIC;

GRANT ALL ON TABLE public.spatial_ref_sys TO postgres;

GRANT SELECT ON TABLE public.spatial_ref_sys TO PUBLIC;