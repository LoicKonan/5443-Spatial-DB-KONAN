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

    # Using that while loop to send a request to the sweep and send the missiles to missiles1.json
    # then after 3 more seconds send to missiles2.json, then stop.
    while True:
        response = requests.get(sweep)
        # print(response.text)
        with open("missile1.json", "w") as f:
            json.dump(response.json(), f, indent=4)

        time.sleep(3)
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
            "CREATE TABLE drop_rate (id SERIAL PRIMARY KEY, missile_id INT, latitude DOUBLE PRECISION, longitude DOUBLE PRECISION, bearing DOUBLE PRECISION, altitude DOUBLE PRECISION, time1 DOUBLE PRECISION, altitude2 DOUBLE PRECISION, time2 DOUBLE PRECISION, drop_rate DOUBLE PRECISION)"
        )
        cur.execute(
            "INSERT INTO drop_rate (missile_id, latitude, longitude, bearing, altitude, time1, altitude2, time2, drop_rate) SELECT missiles1.missile_id, missiles1.latitude, missiles1.longitude, missiles1.bearing, missiles1.altitude, missiles1.time1, missiles2.altitude, missiles2.time2, ABS((missiles2.altitude - missiles1.altitude) / (missiles2.time2 - missiles1.time1)) AS drop_rate FROM missiles1 INNER JOIN missiles2 ON missiles1.missile_id = missiles2.missile_id"
        )

    # drop rate = abs(change in alt / change in time) ms
    # Find the the absolute value of the drop_rate between missile1 and missile2
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "SELECT missiles1.missile_id, missiles1.latitude, missiles1.longitude, missiles1.bearing, missiles1.altitude, missiles1.time1, missiles2.altitude, missiles2.time2, ABS((missiles2.altitude - missiles1.altitude) / (missiles2.time2 - missiles1.time1)) AS drop_rate FROM missiles1 INNER JOIN missiles2 ON missiles1.missile_id = missiles2.missile_id"
        )
        # for row in cur.fetchall():
        #     print(row)

    print("Drop Rate Table Loaded to database.")

    # Here I'm creating a table called time_to_hit_ground then load it to the database.
    # id is a primary key int
    # missile id int
    # latitude double precision
    # longitude double precision
    # bearing double precision
    # altitude double precision
    # current_time int
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "DROP TABLE IF EXISTS time_to_hit_ground;"
            "CREATE TABLE time_to_hit_ground (id SERIAL PRIMARY KEY, m_id INT, latitude DOUBLE PRECISION, longitude DOUBLE PRECISION, bearing DOUBLE PRECISION, altitude DOUBLE PRECISION, time1 DOUBLE PRECISION, altitude2 DOUBLE PRECISION, time2 DOUBLE PRECISION, drop_rate DOUBLE PRECISION, time_to_hit_ground DOUBLE PRECISION)"
        )
        cur.execute(
            "INSERT INTO time_to_hit_ground (m_id, latitude, longitude, bearing, altitude, time1, altitude2, time2, drop_rate, time_to_hit_ground) SELECT missile_id, latitude, longitude, bearing, altitude, time1, altitude2, time2, drop_rate, ABS(altitude / drop_rate) AS time_to_hit_ground FROM drop_rate"
        )

    # how many seconds until it hit the ground = abs (alt / drop rate)
    # Find the time until the missile hits the ground
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "SELECT missile_id, latitude, longitude, bearing, altitude, time1, altitude2, time2, drop_rate, ABS(altitude / drop_rate) AS time_to_hit_ground FROM drop_rate"
        )
        # for row in cur.fetchall():
        #     print(row)
    print("Time to hit ground TABLE loaded to database.")

    # Here I'm creating a table called speed then load it to the database.
    # missile id int
    # latitude double precision
    # longitude double precision
    # bearing double precision
    # altitude double precision
    # current_time int
    # ms double precision
    # missile_type
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "DROP TABLE IF EXISTS speed;"
            "CREATE TABLE speed (missile_id INT, lat DOUBLE PRECISION, lon DOUBLE PRECISION, bear DOUBLE PRECISION, alt DOUBLE PRECISION, time DOUBLE PRECISION, ms DOUBLE PRECISION, missile_type VARCHAR)"
        )
        cur.execute(
            "INSERT INTO speed (missile_id, lat, lon, bear, alt, time, ms, missile_type) SELECT missile_id, latitude, longitude, bearing, altitude, time1, ms, missile_type FROM missiles1 INNER JOIN speed_stuff ON missiles1.missile_type = speed_stuff.type"
        )

        # missile speed
    # Find the speed of the missiles from incoming missiles1.
    # Created a table call (speed_stuff) that is the combination of missile and missile_speed.
    # then compare the type of missile coming to the missile in the speed_stuff. if they equal
    # then add the speed to the new Table call speed.
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "SELECT missile_type, ms FROM missiles1 INNER JOIN speed_stuff ON missiles1.missile_type = speed_stuff.type"
        )
        # for row in cur.fetchall():
        #     print(row)

    print("Speed Table loaded to database.")

    # Here I'm creating a table called exact_location then load it to the database.
    # id is a primary key int
    # missile id int
    # latitude double precision
    # longitude double precision
    # bearing double precision
    # altitude double precision
    # current_time int
    # ms double precision
    # missile_type
    # time_to_hit_ground double precision
    # drop_rate double precision
    # exact_latitude double precision
    # exact_longitude double precision
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "DROP TABLE IF EXISTS exact_location;"
            "CREATE TABLE exact_location (id SERIAL PRIMARY KEY, missile_id INT, lat DOUBLE PRECISION, lon DOUBLE PRECISION, bear DOUBLE PRECISION, alt DOUBLE PRECISION, time DOUBLE PRECISION, ms DOUBLE PRECISION, missile_type VARCHAR, time_to_hit_ground DOUBLE PRECISION, drop_rate DOUBLE PRECISION, exact_latitude DOUBLE PRECISION, exact_longitude DOUBLE PRECISION)"
        )
        cur.execute(
            "INSERT INTO exact_location (missile_id, lat, lon, bear, alt, time, ms, missile_type, time_to_hit_ground, drop_rate, exact_latitude, exact_longitude) SELECT missile_id, lat, lon, bear, alt, time, ms, missile_type, time_to_hit_ground, drop_rate, (lat + (ms * time_to_hit_ground * sin(bear))) AS latitude, (lon + (ms * time_to_hit_ground * cos(bear))) AS longitude FROM speed INNER JOIN time_to_hit_ground ON speed.missile_id = time_to_hit_ground.m_id"
        )

        # Find the exact location that the missile will reach the ground, Calculate when altitude = 0
    # by using the time_hit_ground, altitude and  the drop_rate, using both table called speed and time_hit_ground
    # then add the new location to the table called (exact_location)
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "SELECT missile_id, lat, lon, bear, alt, time, ms, missile_type, time_to_hit_ground, drop_rate, (lat + (ms * time_to_hit_ground * sin(bear))) AS latitude, (lon + (ms * time_to_hit_ground * cos(bear))) AS longitude FROM speed INNER JOIN time_to_hit_ground ON speed.missile_id = time_to_hit_ground.m_id"
        )
        # for row in cur.fetchall():
        #     print(row)

    print("Exact Location Table loaded to database.")

    # Here I'm creating a table called myregion then load it to the database.
    # id is a primary key int
    # myregion geometry
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "DROP TABLE IF EXISTS myregion;"
            "CREATE TABLE myregion (id SERIAL PRIMARY KEY, myregion geometry)"
        )
        cur.execute(
            "INSERT INTO myregion (myregion) SELECT ST_SetSRID(ST_MakeBox2D(ST_Point(-180, -90), ST_Point(180, 90)), 4326) AS myregion;"
        )

        # add a bounding box around my table called myregion
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "SELECT ST_SetSRID(ST_MakeBox2D(ST_Point(-180, -90), ST_Point(180, 90)), 4326) AS myregion;"
        )
        # for row in cur.fetchall():
        #     print(row)

    print("Bounding Box Table loaded to database.")

    # uses postgis st_within to check if the points are in the bounding box table
    # output should be True if the points are in the bounding box table or False otherwise
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "SELECT ST_Within(ST_SetSRID(ST_MakePoint(exact_longitude, exact_latitude), 4326), myregion) FROM exact_location, myregion;"
        )
        # for row in cur.fetchall():
        #     print(row)

    print("Points in Bounding Box Table loaded to database.")

    # Here I'm creating a table called points_in_bounding_box then load it to the database.
    # id is a primary key int
    # points_in_bounding_box boolean
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "DROP TABLE IF EXISTS points_in_bounding_box;"
            "CREATE TABLE points_in_bounding_box (id SERIAL PRIMARY KEY, missile_id INT, lat DOUBLE PRECISION, lon DOUBLE PRECISION, bear DOUBLE PRECISION, alt DOUBLE PRECISION, time DOUBLE PRECISION, ms DOUBLE PRECISION, missile_type VARCHAR, time_to_hit_ground DOUBLE PRECISION, drop_rate DOUBLE PRECISION, exact_latitude DOUBLE PRECISION, exact_longitude DOUBLE PRECISION ,points_in_bounding_box BOOLEAN)"
        )
        cur.execute(
            "INSERT INTO points_in_bounding_box (missile_id, lat, lon, bear, alt, time, ms, missile_type, time_to_hit_ground, drop_rate, exact_latitude, exact_longitude, points_in_bounding_box) SELECT missile_id, lat, lon, bear, alt, time, ms, missile_type, time_to_hit_ground, drop_rate, exact_latitude, exact_longitude, ST_Within(ST_SetSRID(ST_MakePoint(exact_longitude, exact_latitude), 4326), myregion) FROM exact_location, myregion;"
        )

    # uses postgis to get a set of points along the line with the missile for interception
    # output should be a set of points along the line with the missile for interception
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "SELECT ST_LineInterpolatePoints(ST_MakeLine(ST_SetSRID(ST_MakePoint(lon, lat), 4326), ST_SetSRID(ST_MakePoint(exact_longitude, exact_latitude), 4326)), .08) FROM exact_location;"
        )
        for row in cur.fetchall():
            print(row)

    print("Points along the line with the missile for interception loaded to database.")

    # Here I'm creating a table called points_along_line then load it to the database.
    # id is a primary key int
    # points_along_line geometry
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "DROP TABLE IF EXISTS points_along_line;"
            "CREATE TABLE points_along_line (id SERIAL PRIMARY KEY, missile_id INT, lat DOUBLE PRECISION, lon DOUBLE PRECISION, bear DOUBLE PRECISION, alt DOUBLE PRECISION, time DOUBLE PRECISION, ms DOUBLE PRECISION, missile_type VARCHAR, time_to_hit_ground DOUBLE PRECISION, drop_rate DOUBLE PRECISION, exact_latitude DOUBLE PRECISION, exact_longitude DOUBLE PRECISION ,points_in_bounding_box BOOLEAN, points_along_line geometry)"
        )
        cur.execute(
            "INSERT INTO points_along_line (missile_id, lat, lon, bear, alt, time, ms, missile_type, time_to_hit_ground, drop_rate, exact_latitude, exact_longitude, points_in_bounding_box, points_along_line) SELECT missile_id, lat, lon, bear, alt, time, ms, missile_type, time_to_hit_ground, drop_rate, exact_latitude, exact_longitude, ST_Within(ST_SetSRID(ST_MakePoint(exact_longitude, exact_latitude), 4326), myregion), ST_LineInterpolatePoints(ST_MakeLine(ST_SetSRID(ST_MakePoint(lon, lat), 4326), ST_SetSRID(ST_MakePoint(exact_longitude, exact_latitude), 4326)), .08) FROM exact_location, myregion;"
        )

    # the point we want to try and intercept (halfway point)
    # output should be the point we want to try and intercept (halfway point)
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "SELECT ST_AsText(ST_LineInterpolatePoint(ST_MakeLine(ST_SetSRID(ST_MakePoint(lon, lat), 4326), ST_SetSRID(ST_MakePoint(exact_longitude, exact_latitude), 4326)), .5)) FROM exact_location;"
        )
        for row in cur.fetchall():
            print(row)

    # Here I'm creating a table called closest_city then load it to the database.
    # id is a primary key int
    # closest_city geometry
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "DROP TABLE IF EXISTS closest_city;"
            "CREATE TABLE closest_city (id SERIAL PRIMARY KEY, missile_id INT, lat DOUBLE PRECISION, lon DOUBLE PRECISION, bear DOUBLE PRECISION, alt DOUBLE PRECISION, time DOUBLE PRECISION, ms DOUBLE PRECISION, missile_type VARCHAR, time_to_hit_ground DOUBLE PRECISION, drop_rate DOUBLE PRECISION, exact_latitude DOUBLE PRECISION, exact_longitude DOUBLE PRECISION ,points_in_bounding_box BOOLEAN, points_along_line geometry, closest_city geometry)"
        )
        cur.execute(
            "INSERT INTO closest_city (missile_id, lat, lon, bear, alt, time, ms, missile_type, time_to_hit_ground, drop_rate, exact_latitude, exact_longitude, points_in_bounding_box, points_along_line, closest_city) SELECT missile_id, lat, lon, bear, alt, time, ms, missile_type, time_to_hit_ground, drop_rate, exact_latitude, exact_longitude, ST_Within(ST_SetSRID(ST_MakePoint(exact_longitude, exact_latitude), 4326), myregion), ST_LineInterpolatePoints(ST_MakeLine(ST_SetSRID(ST_MakePoint(lon, lat), 4326), ST_SetSRID(ST_MakePoint(exact_longitude, exact_latitude), 4326)), .08), ST_ClosestPoint(ST_SetSRID(ST_MakePoint(lon, lat), 4326), ST_SetSRID(ST_MakePoint(exact_longitude, exact_latitude), 4326)) FROM exact_location, myregion;"
        )

        # gets the closest city to where we want to intercept
    # output should be the closest city to where we want to intercept
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "SELECT ST_AsText(ST_ClosestPoint(ST_SetSRID(ST_MakePoint(lon, lat), 4326), ST_SetSRID(ST_MakePoint(exact_longitude, exact_latitude), 4326))) FROM exact_location;"
        )
        # for row in cur.fetchall():
        #     print(row)

    print("Closest city to where we want to intercept loaded to database.")

    # Number of seconds needed to to destroy incoming missiles.

    # when to fire from battery or city
