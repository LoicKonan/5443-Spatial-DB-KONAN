CREATE TABLE public.missile (
    id numeric NOT NULL,
    missile_type text,
    category numeric,
    speed numeric
);


ALTER TABLE public.missile OWNER TO postgres;


INSERT INTO public.missile (id, missile_type, category, speed) VALUES(0, 'Atlas', 1, 24975);
INSERT INTO public.missile (id, missile_type, category, speed) VALUES(1, 'Harpoon', 2, 27750);
INSERT INTO public.missile (id, missile_type, category, speed) VALUES(2, 'Hellfire', 3, 33300);
INSERT INTO public.missile (id, missile_type, category, speed) VALUES(3, 'Javelin', 4, 36075);
INSERT INTO public.missile (id, missile_type, category, speed) VALUES(4, 'Minuteman',5,38850);
INSERT INTO public.missile (id, missile_type, category, speed) VALUES(5, 'Patriot', 6, 41625);
INSERT INTO public.missile (id, missile_type, category, speed) VALUES(6, 'Peacekeeper', 7, 44400);
INSERT INTO public.missile (id, missile_type, category, speed) VALUES(7, 'SeaSparrow', 8, 47175);
INSERT INTO public.missile (id, missile_type, category, speed) VALUES(8, 'Titan', 8, 47175);
INSERT INTO public.missile (id, missile_type, category, speed) VALUES(9, 'Tomahawk', 9, 49950);
INSERT INTO public.missile (id, missile_type, category, speed) VALUES(10, 'Trident', 9, 49950); 








ALTER TABLE ONLY public.missile
    ADD CONSTRAINT missile_datas_pkey PRIMARY KEY (id);

