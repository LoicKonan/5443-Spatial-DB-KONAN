import time
import requests
import json
from re import S
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
import psycopg2
import json
from geojson import MultiPolygon, Point, MultiPoint


class DatabaseCursor(object):
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


sweep = "http://missilecommand.live:8080/RADAR_SWEEP"

if __name__ == "__main__":

    # Using that while loop to send a request to do the sweep and send the missiles to missiles1.json
    # then after 3 more seconds send to missiles2.json, then stop.
    while True:
        response = requests.get(sweep)
        # print(response.text)
        with open("missile1.json", "w") as f:
            json.dump(response.json(), f, indent=4)

        time.sleep(5)
        response = requests.get(sweep)
        # print(response.text)
        with open("missile2.json", "w") as f:
            json.dump(response.json(), f, indent=4)
        break

    # Here I'm changing the current_time in missile1.json to number of seconds then save it as double precision.
    with open("missile1.json") as f:
        data = json.load(f)
        for i in data["features"]:
            i["properties"]["current_time"] = (
                int(i["properties"]["current_time"][:2]) * 3600
                + int(i["properties"]["current_time"][3:5]) * 60
                + int(i["properties"]["current_time"][6:8])
            )
            # print(i['properties']['current_time'])

        # Here I'm updating the current_time to the new time in the missile1.json
        with open("missile1.json", "w") as f:
            json.dump(data, f, indent=4)

    # Here I'm changing the current_time in missile1.json to number of seconds then save it as double precision.
    with open("missile2.json") as f:
        data = json.load(f)
        for i in data["features"]:
            i["properties"]["current_time"] = (
                int(i["properties"]["current_time"][:2]) * 3600
                + int(i["properties"]["current_time"][3:5]) * 60
                + int(i["properties"]["current_time"][6:8])
            )
            # print(i['properties']['current_time'])

        # Here I'm updating the current_time to the new time in missile1.json
        with open("missile2.json", "w") as f:
            json.dump(data, f, indent=4)

    # Here I'm creating a table called missiles1 from missiles1.json then load it to the database.
    # id is a primary key int
    # missile id int
    # latitude double precision
    # longitude double precision
    # bearing double precision
    # altitude double precision
    # current_time int
    # missile_type string
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "Drop TABLE IF EXISTS missiles1;"
            "CREATE TABLE missiles1 (id SERIAL PRIMARY KEY, missile_id INT, latitude DOUBLE PRECISION, longitude DOUBLE PRECISION, bearing DOUBLE PRECISION, altitude DOUBLE PRECISION, time1 DOUBLE PRECISION, missile_type VARCHAR(255))"
        )

        with open("missile1.json") as f:
            data = json.load(f)
            for i in data["features"]:
                cur.execute(
                    "INSERT INTO missiles1 (missile_id, latitude, longitude, bearing, altitude, time1, missile_type) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (
                        i["id"],
                        i["geometry"]["coordinates"][1],
                        i["geometry"]["coordinates"][0],
                        i["properties"]["bearing"],
                        i["properties"]["altitude"],
                        i["properties"]["current_time"],
                        i["properties"]["missile_type"],
                    ),
                )
    print("Incoming missiles1 loaded successfully")

    # Here I'm creating a table called missiles2 from missiles2.json then load it to the database.
    # id is a primary key int
    # missile id int
    # latitude double precision
    # longitude double precision
    # bearing double precision
    # altitude double precision
    # current_time int
    # missile_type string
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "Drop TABLE IF EXISTS missiles2;"
            "CREATE TABLE missiles2 (id SERIAL PRIMARY KEY, missile_id INT, latitude DOUBLE PRECISION, longitude DOUBLE PRECISION, bearing DOUBLE PRECISION, altitude DOUBLE PRECISION, time2 DOUBLE PRECISION, missile_type VARCHAR(255))"
        )

        with open("missile2.json") as f:
            data = json.load(f)
            for i in data["features"]:
                cur.execute(
                    "INSERT INTO missiles2 (missile_id, latitude, longitude, bearing, altitude, time2, missile_type) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (
                        i["id"],
                        i["geometry"]["coordinates"][1],
                        i["geometry"]["coordinates"][0],
                        i["properties"]["bearing"],
                        i["properties"]["altitude"],
                        i["properties"]["current_time"],
                        i["properties"]["missile_type"],
                    ),
                )

    print("Incoming missiles2 loaded to database.")

    # Here I'm creating a table called drop_rate between missile1 and missile2 then load it to the database.
    # drop_rate = ABS((missiles2.altitude - missiles1.altitude) / (missiles2.time2 - missiles1.time1))
    # missile_type
    # id is a primary key int
    # missile id int
    # latitude double precision
    # longitude double precision
    # bearing double precision
    # altitude double precision
    # current_time int
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "DROP TABLE IF EXISTS drop_rate;"
            "CREATE TABLE drop_rate (id SERIAL PRIMARY KEY, missile_id INT, latitude DOUBLE PRECISION, longitude DOUBLE PRECISION, bearing DOUBLE PRECISION, altitude DOUBLE PRECISION, time1 DOUBLE PRECISION, altitude2 DOUBLE PRECISION, time2 DOUBLE PRECISION, drop_rate DOUBLE PRECISION, missile_type text)"
        )   
        cur.execute(
            "INSERT INTO drop_rate (missile_id, latitude, longitude, bearing, altitude, time1, altitude2, time2, drop_rate, missile_type) SELECT missiles1.missile_id, missiles1.latitude, missiles1.longitude, missiles1.bearing, missiles1.altitude, missiles1.time1, missiles2.altitude, missiles2.time2, ABS((missiles2.altitude - missiles1.altitude) / (missiles2.time2 - missiles1.time1)), missiles1.missile_type FROM missiles1 INNER JOIN missiles2 ON missiles1.missile_id = missiles2.missile_id"
        )
        
    print("Drop rate loaded to database.")
    
    # # Print to console the table Drop rates
    # with DatabaseCursor(".config.json") as cur:
    #     cur.execute("SELECT * FROM drop_rate")
    #     for row in cur.fetchall():
    #         print(row)
        
        
        
    # Here I'm creating a table called speed then load it to the database.
    # In this table i'm adding the speed of the missile from the information giving by the attacking team 
    # from the table call missile in the database then adding it to the TABLE drop_rate. So doing a in join on missile_type.
    # drop_rate 
    # missile_type
    # id is a primary key int
    # missile id int
    # latitude double precision
    # longitude double precision
    # bearing double precision
    # altitude double precision
    # current_time int
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "DROP TABLE IF EXISTS speed;"
            "CREATE TABLE speed (id SERIAL PRIMARY KEY, missile_id INT, latitude DOUBLE PRECISION, longitude DOUBLE PRECISION, bearing DOUBLE PRECISION, altitude DOUBLE PRECISION, time1 DOUBLE PRECISION, altitude2 DOUBLE PRECISION, time2 DOUBLE PRECISION, drop_rate DOUBLE PRECISION, missile_type text, speed DOUBLE PRECISION)"
        )
        cur.execute(
            "INSERT INTO speed (missile_id, latitude, longitude, bearing, altitude, time1, altitude2, time2, drop_rate, missile_type, speed) SELECT drop_rate.missile_id, drop_rate.latitude, drop_rate.longitude, drop_rate.bearing, drop_rate.altitude, drop_rate.time1, drop_rate.altitude2, drop_rate.time2, drop_rate.drop_rate, drop_rate.missile_type, missile.speed FROM drop_rate INNER JOIN missile ON drop_rate.missile_type = missile.missile_type"
        )
        
    print("Speed loaded to database.")
    
    # # Print to console the table speed
    # with DatabaseCursor(".config.json") as cur:
    #     cur.execute("SELECT * FROM speed")
    #     for row in cur.fetchall():
    #         print(row)
    
     

    # Here I'm creating a table called time_missile_ground then load it to the database.
    # Find when will altitude be zero
    # time_missile_ground => when will altitude be zero
    # time_missile_ground = drop_rate / altitude
    # drop_rate 
    # missile_type
    # id is a primary key int
    # missile id int
    # latitude double precision
    # longitude double precision
    # bearing double precision
    # altitude double precision
    # current_time int
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "DROP TABLE IF EXISTS time_missile_ground;"
            "CREATE TABLE time_missile_ground (id SERIAL PRIMARY KEY, missile_id INT, latitude DOUBLE PRECISION, longitude DOUBLE PRECISION, bearing DOUBLE PRECISION, altitude DOUBLE PRECISION, time1 DOUBLE PRECISION, altitude2 DOUBLE PRECISION, time2 DOUBLE PRECISION, drop_rate DOUBLE PRECISION, missile_type text, speed DOUBLE PRECISION, time_missile_ground DOUBLE PRECISION)"
        )
        cur.execute(
            "INSERT INTO time_missile_ground (missile_id, latitude, longitude, bearing, altitude, time1, altitude2, time2, drop_rate, missile_type, speed, time_missile_ground) SELECT speed.missile_id, speed.latitude, speed.longitude, speed.bearing, speed.altitude, speed.time1, speed.altitude2, speed.time2, speed.drop_rate, speed.missile_type, speed.speed, speed.altitude / speed.drop_rate FROM speed"
        )
        
    print("The amount of seconds required for the  missile to hit the ground is loaded to database.")
    
    # # Print to console the table time_missile_ground
    # with DatabaseCursor(".config.json") as cur:
    #     cur.execute("SELECT * FROM time_missile_ground")
    #     for row in cur.fetchall():
    #         print(row)
    
    
    
    # Here I'm creating a table called where_missile_ground then load it to the database.
    # Find the longitude and latitude of where the missile will it the ground.
    # uses postgis project to get the exact location that the missile will reach alt = 0
    # SELECT ST_Project('POINT(" ")'::geography)
    # where_missile_ground => where will the missile hit the ground
    # drop_rate
    # missile_type
    # id is a primary key int
    # missile id int
    # latitude double precision
    # longitude double precision
    # bearing double precision
    # altitude double precision
    # current_time int
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "DROP TABLE IF EXISTS where_missile_ground;"
            "CREATE TABLE where_missile_ground (id SERIAL PRIMARY KEY, missile_id INT, latitude DOUBLE PRECISION, longitude DOUBLE PRECISION, bearing DOUBLE PRECISION, altitude DOUBLE PRECISION, time1 DOUBLE PRECISION, altitude2 DOUBLE PRECISION, time2 DOUBLE PRECISION, drop_rate DOUBLE PRECISION, missile_type text, speed DOUBLE PRECISION, time_missile_ground DOUBLE PRECISION, where_missile_ground GEOGRAPHY)"
        )
        cur.execute(
            "INSERT INTO where_missile_ground (missile_id, latitude, longitude, bearing, altitude, time1, altitude2, time2, drop_rate, missile_type, speed, time_missile_ground, where_missile_ground) SELECT time_missile_ground.missile_id, time_missile_ground.latitude, time_missile_ground.longitude, time_missile_ground.bearing, time_missile_ground.altitude, time_missile_ground.time1, time_missile_ground.altitude2, time_missile_ground.time2, time_missile_ground.drop_rate, time_missile_ground.missile_type, time_missile_ground.speed, time_missile_ground.time_missile_ground, ST_Project(ST_MakePoint(time_missile_ground.longitude, time_missile_ground.latitude), time_missile_ground.time_missile_ground * time_missile_ground.speed, time_missile_ground.bearing) FROM time_missile_ground"
        )
        
    print("The exact location of where the missile will hit the ground is loaded to database.")
    
    # # Print to console the table where_missile_ground
    # with DatabaseCursor(".config.json") as cur:
    #     cur.execute("SELECT * FROM where_missile_ground")
    #     for row in cur.fetchall():
    #         print(row)
    
    
    

    # uses postgis st_within to check if the where_missile_ground are in myregion table from the database.
    # if the point (where_missile_ground) are in myregion then it will be added to the table called in_myregion
    
    
    
    
    
    










    # # uses postgis to get a set of points along the line with the missile for interception
    # # output should be a set of points along the line with the missile for interception
    # with DatabaseCursor(".config.json") as cur:
    #     cur.execute(
    #         "SELECT ST_LineInterpolatePoints(ST_MakeLine(ST_SetSRID(ST_MakePoint(lon, lat), 4326), ST_SetSRID(ST_MakePoint(exact_longitude, exact_latitude), 4326)), .08) FROM exact_location;"
    #     )
    #     for row in cur.fetchall():
    #         print(row)

    # print("Points along the line with the missile for interception loaded to database.")

    # # Here I'm creating a table called points_along_line then load it to the database.
    # # id is a primary key int
    # # points_along_line geometry
    # with DatabaseCursor(".config.json") as cur:
    #     cur.execute(
    #         "DROP TABLE IF EXISTS points_along_line;"
    #         "CREATE TABLE points_along_line (id SERIAL PRIMARY KEY, missile_id INT, lat DOUBLE PRECISION, lon DOUBLE PRECISION, bear DOUBLE PRECISION, alt DOUBLE PRECISION, time DOUBLE PRECISION, ms DOUBLE PRECISION, missile_type VARCHAR, time_missile_ground DOUBLE PRECISION, drop_rate DOUBLE PRECISION, exact_latitude DOUBLE PRECISION, exact_longitude DOUBLE PRECISION ,points_in_bounding_box BOOLEAN, points_along_line geometry)"
    #     )
    #     cur.execute(
    #         "INSERT INTO points_along_line (missile_id, lat, lon, bear, alt, time, ms, missile_type, time_missile_ground, drop_rate, exact_latitude, exact_longitude, points_in_bounding_box, points_along_line) SELECT missile_id, lat, lon, bear, alt, time, ms, missile_type, time_missile_ground, drop_rate, exact_latitude, exact_longitude, ST_Within(ST_SetSRID(ST_MakePoint(exact_longitude, exact_latitude), 4326), myregion), ST_LineInterpolatePoints(ST_MakeLine(ST_SetSRID(ST_MakePoint(lon, lat), 4326), ST_SetSRID(ST_MakePoint(exact_longitude, exact_latitude), 4326)), .08) FROM exact_location, myregion;"
    #     )










    # # the point we want to try and intercept (halfway point)
    # # output should be the point we want to try and intercept (halfway point)
    # with DatabaseCursor(".config.json") as cur:
    #     cur.execute(
    #         "SELECT ST_AsText(ST_LineInterpolatePoint(ST_MakeLine(ST_SetSRID(ST_MakePoint(lon, lat), 4326), ST_SetSRID(ST_MakePoint(exact_longitude, exact_latitude), 4326)), .5)) FROM exact_location;"
    #     )
    #     for row in cur.fetchall():
    #         print(row)

    # # Here I'm creating a table called closest_city then load it to the database.
    # # id is a primary key int
    # # closest_city geometry
    # with DatabaseCursor(".config.json") as cur:
    #     cur.execute(
    #         "DROP TABLE IF EXISTS closest_city;"
    #         "CREATE TABLE closest_city (id SERIAL PRIMARY KEY, missile_id INT, lat DOUBLE PRECISION, lon DOUBLE PRECISION, bear DOUBLE PRECISION, alt DOUBLE PRECISION, time DOUBLE PRECISION, ms DOUBLE PRECISION, missile_type VARCHAR, time_missile_ground DOUBLE PRECISION, drop_rate DOUBLE PRECISION, exact_latitude DOUBLE PRECISION, exact_longitude DOUBLE PRECISION ,points_in_bounding_box BOOLEAN, points_along_line geometry, closest_city geometry)"
    #     )
    #     cur.execute(
    #         "INSERT INTO closest_city (missile_id, lat, lon, bear, alt, time, ms, missile_type, time_missile_ground, drop_rate, exact_latitude, exact_longitude, points_in_bounding_box, points_along_line, closest_city) SELECT missile_id, lat, lon, bear, alt, time, ms, missile_type, time_missile_ground, drop_rate, exact_latitude, exact_longitude, ST_Within(ST_SetSRID(ST_MakePoint(exact_longitude, exact_latitude), 4326), myregion), ST_LineInterpolatePoints(ST_MakeLine(ST_SetSRID(ST_MakePoint(lon, lat), 4326), ST_SetSRID(ST_MakePoint(exact_longitude, exact_latitude), 4326)), .08), ST_ClosestPoint(ST_SetSRID(ST_MakePoint(lon, lat), 4326), ST_SetSRID(ST_MakePoint(exact_longitude, exact_latitude), 4326)) FROM exact_location, myregion;"
    #     )









    #     # gets the closest city to where we want to intercept
    # # output should be the closest city to where we want to intercept
    # with DatabaseCursor(".config.json") as cur:
    #     cur.execute(
    #         "SELECT ST_AsText(ST_ClosestPoint(ST_SetSRID(ST_MakePoint(lon, lat), 4326), ST_SetSRID(ST_MakePoint(exact_longitude, exact_latitude), 4326))) FROM exact_location;"
    #     )
    #     # for row in cur.fetchall():
    #     #     print(row)










    # print("Closest city to where we want to intercept loaded to database.")

    # # Number of seconds needed to to destroy incoming missiles.

    # # when to fire from battery or city
