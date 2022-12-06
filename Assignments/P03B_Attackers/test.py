import json
from rich import pretty
import psycopg2
from random import randint

"""          MAKE SQL TABLE of MISSILE TRAJECTORIES       """
def is_integer(n):
    try:
        int(n)
    except ValueError:
        return False
    return True


def is_float(n):
    try:
        float(n)
    except ValueError:
        return False
    return True


class DatabaseCursor(object):
    """https://stackoverflow.com/questions/32812463/setting-schema-for-all-queries-of-a-connection-in-psycopg2-getting-race-conditi
    https://stackoverflow.com/questions/1984325/explaining-pythons-enter-and-exit
    """

    def __init__(self, conn_config_file):
        with open(conn_config_file) as config_file:
            self.conn_config = json.load(config_file)

    def __enter__(self):
        self.conn = psycopg2.connect(
            "dbname='"
            + self.conn_config["dbname"]
            + "' "
            + "user='"
            + self.conn_config["user"]
            + "' "
            + "host='"
            + self.conn_config["host"]
            + "' "
            + "password='"
            + self.conn_config["password"]
            + "' "
            + "port="
            + self.conn_config["port"]
            + " "
        )
        self.cur = self.conn.cursor()
        self.cur.execute("SET search_path TO " + self.conn_config["schema"])

        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        # some logic to commit/rollback
        self.conn.commit()
        self.conn.close()


if __name__ == "__main__":
    
    with DatabaseCursor('.config.json') as cur:
        #Fill table with missile trajectories based on coordinate pairs
        sql = f"""SELECT * FROM public.cities WHERE ST_Intersects(location, '{self.region}::geometry');"""

        cur.execute(sql)
        cur.execute("""SELECT json_build_object(
            'type', 'FeatureCollection',
            'features', json_agg(ST_AsGeoJSON(t.*)::json)
            )
            FROM public.missile_trajectories
            as t(id, name, geom);""")

        trajectories = cur.fetchall()
        print(trajectories)


