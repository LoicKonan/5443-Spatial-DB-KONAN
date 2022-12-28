import json
import psycopg2
import geojson

'#########################################################################################'
'                                  Database Implementation                                '
'#########################################################################################'

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


drop_table = "DROP TABLE  IF EXISTS cities;"

create_table = """CREATE TABLE public.cities (
    id NUMERIC PRIMARY KEY,
    latitude DECIMAL(11,8) NOT NULL,
    longitude DECIMAL(11,8) NOT NULL,
    location GEOMETRY(POINT,4326));"""


if __name__ == "__main__":
    
    #Importing the csv data into the database and cleaning up the data as well

    with DatabaseCursor('.config.json') as cur:
        cur.execute(drop_table)
        cur.execute(create_table)

        with open("uspoints.geojson", newline="") as f:
            points = geojson.load(f)
            counter = 0
            for point in points['features']:
                id = counter
                lon = point['geometry']['coordinates'][1]
                lat = point['geometry']['coordinates'][0]

                counter += 1
                row = f"{id}, {lon}, {lat}"
                sql = f"INSERT INTO public.cities VALUES ({row});"
                cur.execute(sql)

        update_location = """UPDATE public.cities
        SET location = ST_SetSRID(ST_MakePoint(longitude,latitude), 4326);"""
        cur.execute(update_location)

        cur.execute("""SELECT json_build_object(
            'type', 'FeatureCollection',
            'features', json_agg(ST_AsGeoJSON(t.*)::json)
            )
            FROM public.cities
            as t(id, latitude, longitude, geom);""")

        trajectories = cur.fetchall()

        with open('newcitypoints.geojson', "w") as f:
            json.dump(trajectories[0][0], f)

        