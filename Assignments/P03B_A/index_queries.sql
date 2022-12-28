CREATE INDEX cities_idx
ON cities (id);

CREATE INDEX mis_name_idx
ON missile (name);

CREATE INDEX mis_blast_idx
ON missile_blast (blast_radius);

CREATE INDEX mis_data_idx
ON missile_data (missile_id);

CREATE INDEX mis_speed_idx
ON missile_speed (mph);

CREATE INDEX participant_idx
ON participants (id);

CREATE INDEX gid_idx
ON regions_simple (gid);