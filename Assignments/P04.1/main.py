import geojson
import json
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse,HTMLResponse 
import psycopg2
import json
from geojson import Polygon, Point, MultiPoint


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
    
    cardDir = ["N","NNE","NE","ENE","E","ESE","SE","SSE", "S","SSW","SW","WSW","W","WNW","NW","NNW"]
    cardDeg = [0, 22.5, 45, 67.5, 90, 112.5, 135, 157.5, 180, 202.5, 225, 247.5, 270, 292.5, 315, 337.5]
    cardMax = [348.75, 11.25, 33.75, 56.25, 78.75, 101.25, 123.75, 146.25, 168.75, 191.25, 213.75, 236.25, 258.75, 281.25, 303.75, 326.25]
    cardMin = [11.25, 33.75, 56.25, 78.75, 101.25, 123.75, 146.25, 168.75, 191.25, 213.75, 236.25, 258.75, 281.25, 303.75, 326.25, 348.75]


    shipCount = 0
    
    with open("ships.json", "r") as f:
        ships = json.loads(f.read())
        for ship in ships:
            shipCount += 1
            tor = json.dumps(ship["torpedoLaunchers"])
            armame = json.dumps(ship["armament"])
            arma = json.dumps(ship["armor"])

            #print(tor)
            sql = f"""
            INSERT INTO ship (ship_id, category, shipclass, length, width, torpedolaunchers, armament, armor, speed, turn_radius)
            VALUES ({ship["id"]}, '{ship["category"]}', '{ship["shipClass"]}', {ship["length"]}, {ship["width"]}, '{tor}', '{armame}', '{arma}', {ship["speed"]}, {ship["turn_radius"]}
            )
            """
            with DatabaseCursor(".config.json") as cur:
                pass
                res = cur.execute(sql)
                # answer = cur.fetchall()

                print(res)


    table_sql = """
    
    CREATE TABLE public.ship (
    ship_id numeric NOT NULL,
    category text,
    shipclass text,
    displacement numeric,
    length numeric,
    width numeric,
    torpedolaunchers json,
    armament json,
    armor json,
    speed numeric,
    turn_radius numeric
);
    """

    with DatabaseCursor(".config.json") as cur:
            res = cur.execute(table_sql)
            #answer = cur.fetchall()

            print(res)
    
    
    # Bounding Box Shit
    
    """

        Bounding Box dimensions
        
        {
            "UpperLeft": {"lon": -10.31324002, "lat": 50.17116998},
            "LowerRight": {"lon": -8.06068579, "lat": 48.74631646},
        }
        
        geometry ST_MakeEnvelope(float xmin, float ymin, float xmax, float ymax, integer srid=unknown);
    """
    
    bb_Query = "SELECT ST_AsGeoJson(ST_MakeEnvelope(-10.31324002, 48.74631646, -8.06068579, 50.17116998, 4326));"
    
    ## ^^^^ That should generate the bounding box region from Slack
    ## Now need to generate a random or random points in the region
    
    ## This could in theory generate random points based on the # of ships read in
    randomPointsQuery = """SELECT ST_GeneratePoints(geom, {bb_Query}, {shipCount});"""
    
    """ 
        Or we could use this: geometry ST_Centroid(geometry g1);
        
        Generate a central point in the bounding box and then add some deviation to the points
    """