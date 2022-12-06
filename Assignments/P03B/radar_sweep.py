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
import datetime


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
    # then after some seconds send to missiles2.json, then stop.
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

    # Make the missiles2_geom table into geometry
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "DROP TABLE IF EXISTS missiles2_geom;"
            "CREATE TABLE missiles2_geom AS SELECT id, missile_id, ST_SetSRID(ST_MakePoint(longitude, latitude), 4326) AS geom, bearing, altitude, time2, missile_type FROM missiles2;"
        )

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

    print(
        "The amount of seconds required for the  missile to hit the ground is loaded to database."
    )

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
            "CREATE TABLE where_missile_ground (id SERIAL PRIMARY KEY, missile_id INT, latitude DOUBLE PRECISION, longitude DOUBLE PRECISION, bearing DOUBLE PRECISION, altitude DOUBLE PRECISION, time1 DOUBLE PRECISION, altitude2 DOUBLE PRECISION, time2 DOUBLE PRECISION, drop_rate DOUBLE PRECISION, missile_type text, speed DOUBLE PRECISION, time_missile_ground DOUBLE PRECISION, where_missile_ground geography)"
        )
        cur.execute(
            "INSERT INTO where_missile_ground (missile_id, latitude, longitude, bearing, altitude, time1, altitude2, time2, drop_rate, missile_type, speed, time_missile_ground, where_missile_ground) SELECT time_missile_ground.missile_id, time_missile_ground.latitude, time_missile_ground.longitude, time_missile_ground.bearing, time_missile_ground.altitude, time_missile_ground.time1, time_missile_ground.altitude2, time_missile_ground.time2, time_missile_ground.drop_rate, time_missile_ground.missile_type, time_missile_ground.speed, time_missile_ground.time_missile_ground, ST_Project(ST_MakePoint(time_missile_ground.longitude, time_missile_ground.latitude), time_missile_ground.time_missile_ground * time_missile_ground.speed, time_missile_ground.bearing) FROM time_missile_ground"
        )

    print(
        "The exact location of where the missile will hit the ground is loaded to database."
    )

    # # Print to console the table where_missile_ground
    # with DatabaseCursor(".config.json") as cur:
    #     cur.execute("SELECT * FROM where_missile_ground")
    #     for row in cur.fetchall():
    #         print(row)

    # CREATE TABLE call where_missile_ground_geom which will cast the where_missile_ground
    # from geography to geometry
    # using geog:: geometry
    # where_missile_ground_geom => where will the missile hit the ground
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "DROP TABLE IF EXISTS where_missile_ground_geom;"
            "CREATE TABLE where_missile_ground_geom (id SERIAL PRIMARY KEY, missile_id INT, latitude DOUBLE PRECISION, longitude DOUBLE PRECISION, bearing DOUBLE PRECISION, altitude DOUBLE PRECISION, time1 DOUBLE PRECISION, altitude2 DOUBLE PRECISION, time2 DOUBLE PRECISION, drop_rate DOUBLE PRECISION, missile_type text, speed DOUBLE PRECISION, time_missile_ground DOUBLE PRECISION, where_missile_ground geography, where_missile_ground_geom geometry)"
        )
        cur.execute(
            "INSERT INTO where_missile_ground_geom (missile_id, latitude, longitude, bearing, altitude, time1, altitude2, time2, drop_rate, missile_type, speed, time_missile_ground, where_missile_ground, where_missile_ground_geom) SELECT where_missile_ground.missile_id, where_missile_ground.latitude, where_missile_ground.longitude, where_missile_ground.bearing, where_missile_ground.altitude, where_missile_ground.time1, where_missile_ground.altitude2, where_missile_ground.time2, where_missile_ground.drop_rate, where_missile_ground.missile_type, where_missile_ground.speed, where_missile_ground.time_missile_ground, where_missile_ground.where_missile_ground, where_missile_ground.where_missile_ground::geometry FROM where_missile_ground"
        )

    # Create a table call missile line that will make a line between the points missiles2_geom
    # where_missile_ground_geom
    # missile_line => line between the missile and where it will hit the ground
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "DROP TABLE IF EXISTS missile_line;"
            "CREATE TABLE missile_line (id SERIAL PRIMARY KEY, missile_id INT, latitude DOUBLE PRECISION, longitude DOUBLE PRECISION, bearing DOUBLE PRECISION, altitude DOUBLE PRECISION, time1 DOUBLE PRECISION, altitude2 DOUBLE PRECISION, time2 DOUBLE PRECISION, drop_rate DOUBLE PRECISION, missile_type text, speed DOUBLE PRECISION, time_missile_ground DOUBLE PRECISION, where_missile_ground geography, where_missile_ground_geom geometry, missile_line geometry)"
        )
        cur.execute(
            "INSERT INTO missile_line (missile_id, latitude, longitude, bearing, altitude, time1, altitude2, time2, drop_rate, missile_type, speed, time_missile_ground, where_missile_ground, where_missile_ground_geom, missile_line) SELECT where_missile_ground_geom.missile_id, where_missile_ground_geom.latitude, where_missile_ground_geom.longitude, where_missile_ground_geom.bearing, where_missile_ground_geom.altitude, where_missile_ground_geom.time1, where_missile_ground_geom.altitude2, where_missile_ground_geom.time2, where_missile_ground_geom.drop_rate, where_missile_ground_geom.missile_type, where_missile_ground_geom.speed, where_missile_ground_geom.time_missile_ground, where_missile_ground_geom.where_missile_ground, where_missile_ground_geom.where_missile_ground_geom, ST_MakeLine(missiles2_geom.geom, where_missile_ground_geom.where_missile_ground_geom) FROM where_missile_ground_geom, missiles2_geom WHERE where_missile_ground_geom.missile_id = missiles2_geom.missile_id"
        )

    # Create a table call missiles_points which are points along the missile_line
    # of missile_line using ST_LineInterpolatePoints
    # id SERIAL PRIMARY KEY
    # missile_id INT
    # bearing DOUBLE PRECISION
    # drop_rate DOUBLE PRECISION
    # missile_type text
    # speed DOUBLE PRECISION
    # time_missile_ground DOUBLE PRECISION
    # where_missile_ground_geom geometry
    # missile_line geometry
    # missiles_points geometry
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "DROP TABLE IF EXISTS missiles_points;"
            "CREATE TABLE missiles_points (id SERIAL PRIMARY KEY, missile_id INT, bearing DOUBLE PRECISION, drop_rate DOUBLE PRECISION, missile_type text, speed DOUBLE PRECISION, time_missile_ground DOUBLE PRECISION, where_missile_ground_geom geometry, missile_line geometry, missiles_points geometry)"
        )
        cur.execute(
            "INSERT INTO missiles_points (missile_id, bearing, drop_rate, missile_type, speed, time_missile_ground, where_missile_ground_geom, missile_line, missiles_points) SELECT missile_line.missile_id, missile_line.bearing, missile_line.drop_rate, missile_line.missile_type, missile_line.speed, missile_line.time_missile_ground, missile_line.where_missile_ground_geom, missile_line.missile_line, ST_LineInterpolatePoints(missile_line.missile_line, 0.25) FROM missile_line"
        )

    # uses postgis to check if the missile_lines intersects myregion.geom
    # if it does then insert the missile_id into the table called danger_closing
    # danger_closing => missiles that are in myregion
    # danger_closing boolean
    # return the ones that are true.
    # the their geometry location.
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "DROP TABLE IF EXISTS danger_closing;"
            "CREATE TABLE danger_closing (id SERIAL PRIMARY KEY, missile_id INT, danger_closing boolean, missile_line geometry)"
        )
        cur.execute(
            "INSERT INTO danger_closing (missile_id, danger_closing, missile_line) SELECT missile_line.missile_id, ST_Intersects(missile_line.missile_line, myregion.geom), missile_line.missile_line FROM missile_line, myregion WHERE ST_Intersects(missile_line.missile_line, myregion.geom) = true"
        )

    # Create a table call missiles_Intersects which are points along the danger_closing
    # using ST_LineInterpolatePoints
    # id SERIAL PRIMARY KEY
    # missile_id INT
    # danger_closing boolean
    # missile_line geometry
    # missiles_Intersects geometry
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "DROP TABLE IF EXISTS missiles_Intersects;"
            "CREATE TABLE missiles_Intersects (id SERIAL PRIMARY KEY, missile_id INT, danger_closing boolean, missile_line geometry, missiles_Intersects geometry)"
        )
        cur.execute(
            "INSERT INTO missiles_Intersects (missile_id, danger_closing, missile_line, missiles_Intersects) SELECT danger_closing.missile_id, danger_closing.danger_closing, danger_closing.missile_line, ST_LineInterpolatePoints(danger_closing.missile_line, 0.25) FROM danger_closing"
        )

    # Find the last(JUST CHANGED IT) points of the line using st_line_interpolate_point from the missiles_intersects.missile_line
    # id SERIAL PRIMARY KEY
    # missile_id INT
    # danger_closing boolean
    # missile_line geometry
    # missiles_Intersects geometry
    # missiles_Intersects_middle geometry
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "DROP TABLE IF EXISTS missiles_Intersects_middle;"
            "CREATE TABLE missiles_Intersects_middle (id SERIAL PRIMARY KEY, missile_id INT, danger_closing boolean, missile_line geometry, missiles_Intersects geometry, missiles_Intersects_middle geometry)"
        )
        cur.execute(
            "INSERT INTO missiles_Intersects_middle (missile_id, danger_closing, missile_line, missiles_Intersects, missiles_Intersects_middle) SELECT missiles_Intersects.missile_id, missiles_Intersects.danger_closing, missiles_Intersects.missile_line, missiles_Intersects.missiles_Intersects, ST_LineInterpolatePoint(missiles_Intersects.missile_line, .1) FROM missiles_Intersects"
        )

    # Find the longitude and latitude of missiles_intersects_middle
    # id SERIAL PRIMARY KEY
    # missile_id INT
    # danger_closing boolean
    # missile_line geometry
    # missiles_Intersects geometry
    # missiles_Intersects_middle geometry
    # longitude DOUBLE PRECISION
    # latitude DOUBLE PRECISION
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "DROP TABLE IF EXISTS missiles_Intersects_middle_lon_lat;"
            "CREATE TABLE missiles_Intersects_middle_lon_lat (id SERIAL PRIMARY KEY, missile_id INT, danger_closing boolean, missile_line geometry, missiles_Intersects geometry, missiles_Intersects_middle geometry, longitude DOUBLE PRECISION, latitude DOUBLE PRECISION)"
        )
        cur.execute(
            "INSERT INTO missiles_Intersects_middle_lon_lat (missile_id, danger_closing, missile_line, missiles_Intersects, missiles_Intersects_middle, longitude, latitude) SELECT missiles_Intersects_middle.missile_id, missiles_Intersects_middle.danger_closing, missiles_Intersects_middle.missile_line, missiles_Intersects_middle.missiles_Intersects, missiles_Intersects_middle.missiles_Intersects_middle, ST_X(missiles_Intersects_middle.missiles_Intersects_middle), ST_Y(missiles_Intersects_middle.missiles_Intersects_middle) FROM missiles_Intersects_middle"
        )

    # Finding the longitude and latitude of our battery
    # battery.geom is geometry
    # battery.longitude is double precision
    # battery.latitude is double precision
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "DROP TABLE IF EXISTS battery_lon_lat;"
            "CREATE TABLE battery_lon_lat (id SERIAL PRIMARY KEY, geom geometry, longitude DOUBLE PRECISION, latitude DOUBLE PRECISION)"
        )
        cur.execute(
            "INSERT INTO battery_lon_lat (geom, longitude, latitude) SELECT geom, ST_X(geom), ST_Y(geom) FROM battery"
        )

    # Project a line from the battery to the missiles_intersects_middle_lon_lat point and return the intersection points, the distance.
    # missile_id INT
    # missiles_Intersects geometry
    # missiles_Intersects_middle geometry
    # longitude DOUBLE PRECISION
    # latitude DOUBLE PRECISION
    # battery_lon_lat_geom geometry
    # point_to_shoot_lon DOUBLE PRECISION
    # point_to_shoot_lat DOUBLE PRECISION
    # point_to_shoot geometry
    # distance DOUBLE PRECISION
    # distance_line geometry
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "DROP TABLE IF EXISTS point_to_shoot;"
            "CREATE TABLE point_to_shoot (id SERIAL PRIMARY KEY, missile_id INT, missiles_Intersects geometry, missiles_Intersects_middle geometry, longitude DOUBLE PRECISION, latitude DOUBLE PRECISION, battery_lon_lat_geom geometry, point_to_shoot_lon DOUBLE PRECISION, point_to_shoot_lat DOUBLE PRECISION, point_to_shoot geometry, distance DOUBLE PRECISION, distance_line geometry)"
        )
        cur.execute(
            "INSERT INTO point_to_shoot (missile_id, missiles_Intersects, missiles_Intersects_middle, longitude, latitude, battery_lon_lat_geom, point_to_shoot_lon, point_to_shoot_lat, point_to_shoot, distance, distance_line) SELECT missiles_Intersects_middle_lon_lat.missile_id, missiles_Intersects_middle_lon_lat.missiles_Intersects, missiles_Intersects_middle_lon_lat.missiles_Intersects_middle, missiles_Intersects_middle_lon_lat.longitude, missiles_Intersects_middle_lon_lat.latitude, battery_lon_lat.geom, ST_X(ST_LineInterpolatePoint(ST_MakeLine(battery_lon_lat.geom, missiles_Intersects_middle_lon_lat.missiles_Intersects_middle), 0.75)), ST_Y(ST_LineInterpolatePoint(ST_MakeLine(battery_lon_lat.geom, missiles_Intersects_middle_lon_lat.missiles_Intersects_middle), 0.75)), ST_LineInterpolatePoint(ST_MakeLine(battery_lon_lat.geom, missiles_Intersects_middle_lon_lat.missiles_Intersects_middle), 0.75), ST_Distance(battery_lon_lat.geom, missiles_Intersects_middle_lon_lat.missiles_Intersects_middle), ST_MakeLine(battery_lon_lat.geom, missiles_Intersects_middle_lon_lat.missiles_Intersects_middle) FROM missiles_Intersects_middle_lon_lat, battery_lon_lat"
        )

    # Make a table call point_to_shoot_altitude that will Find the altitude of the missile at this point (missiles_Intersects_middle geometry)
    # using the drop_rate from drop_rate table and the time from time_missile_ground.
    # id SERIAL PRIMARY KEY
    # missile_id INT
    # Altitude = drop_rate * (time_missile_ground / 7)
    # drop_rate DOUBLE PRECISION
    # time_missile_ground DOUBLE PRECISION
    # missiles_Intersects_middle geometry
    # altitude DOUBLE PRECISION
    # altitude geom
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "DROP TABLE IF EXISTS point_to_shoot_altitude;"
            "CREATE TABLE point_to_shoot_altitude (id SERIAL PRIMARY KEY, missile_id INT, drop_rate DOUBLE PRECISION, time_missile_ground DOUBLE PRECISION, missiles_Intersects_middle geometry, altitude DOUBLE PRECISION, altitude_geom geometry)"
        )
        cur.execute(
            "INSERT INTO point_to_shoot_altitude (missile_id, drop_rate, time_missile_ground, missiles_Intersects_middle, altitude, altitude_geom) SELECT point_to_shoot.missile_id, drop_rate.drop_rate, time_missile_ground.time_missile_ground, point_to_shoot.missiles_Intersects_middle, drop_rate.drop_rate * (time_missile_ground.time_missile_ground / 7), ST_SetSRID(ST_MakePoint(ST_X(point_to_shoot.missiles_Intersects_middle), ST_Y(point_to_shoot.missiles_Intersects_middle), drop_rate.drop_rate * (time_missile_ground.time_missile_ground / 7)), 4326) FROM point_to_shoot, drop_rate, time_missile_ground WHERE point_to_shoot.missile_id = drop_rate.missile_id AND point_to_shoot.missile_id = time_missile_ground.missile_id"
        )

    # Make a table to get the point_to_shoot_altitude_distance
    # calculate the distance between the point_to_shoot_altitude and our battery location
    # id SERIAL PRIMARY KEY
    # missile_id INT
    # missiles_Intersects_middle geometry
    # point_to_shoot_altitude geometry
    # distance DOUBLE PRECISION
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "DROP TABLE IF EXISTS point_to_shoot_altitude_distance;"
            "CREATE TABLE point_to_shoot_altitude_distance (id SERIAL PRIMARY KEY, missile_id INT, missiles_Intersects_middle geometry, point_to_shoot_altitude geometry, distance DOUBLE PRECISION)"
        )
        cur.execute(
            "INSERT INTO point_to_shoot_altitude_distance (missile_id, missiles_Intersects_middle, point_to_shoot_altitude, distance) SELECT point_to_shoot_altitude.missile_id, point_to_shoot_altitude.missiles_Intersects_middle, point_to_shoot_altitude.altitude_geom, ST_Distance(point_to_shoot_altitude.altitude_geom, battery_lon_lat.geom) FROM point_to_shoot_altitude, battery_lon_lat"
        )

    # This table is used to calculate the Number of seconds to destroy the missile.
    # We shooting a missile from our battery location(longitude and latitude) to
    # this point(missiles_Intersects_middle geometry)
    # we know the distance from the battery to the point(missiles_Intersects_middle geometry)
    # and the speed of the missile => Trident ( using this as speed of the missile 49950)
    # we can calculate the time to reach the point(missiles_Intersects_middle geometry)
    # id SERIAL PRIMARY KEY
    # missile_id INT
    # missiles_Intersects_middle geometry
    # distance DOUBLE PRECISION
    # speed_missile DOUBLE PRECISION
    # time DOUBLE PRECISION
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "DROP TABLE IF EXISTS numb_sec_reach_missile;"
            "CREATE TABLE numb_sec_reach_missile (id SERIAL PRIMARY KEY, missile_id INT, missiles_Intersects_middle geometry, distance DOUBLE PRECISION, speed_missile DOUBLE PRECISION, time DOUBLE PRECISION)"
        )
        cur.execute(
            "INSERT INTO numb_sec_reach_missile (missile_id, missiles_Intersects_middle, distance, speed_missile, time) SELECT point_to_shoot_altitude_distance.missile_id, point_to_shoot_altitude_distance.missiles_Intersects_middle, point_to_shoot_altitude_distance.distance, 49950, point_to_shoot_altitude_distance.distance / 49950 FROM point_to_shoot_altitude_distance"
        )

    # Add numb_sec_reach_missile.time to the missiles2.time2
    # id SERIAL PRIMARY KEY
    # missile_id INT
    # missiles_Intersects_middle geometry
    # distance DOUBLE PRECISION
    # time DOUBLE PRECISION
    # time2 DOUBLE PRECISION
    # return_time
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "DROP TABLE IF EXISTS return_time;"
            "CREATE TABLE return_time (id SERIAL PRIMARY KEY, missile_id INT, missiles_Intersects_middle geometry, distance DOUBLE PRECISION, time DOUBLE PRECISION, time2 DOUBLE PRECISION, return_time DOUBLE PRECISION)"
        )
        cur.execute(
            "INSERT INTO return_time (missile_id, missiles_Intersects_middle, distance, time, time2, return_time) SELECT numb_sec_reach_missile.missile_id, numb_sec_reach_missile.missiles_Intersects_middle, numb_sec_reach_missile.distance, numb_sec_reach_missile.time, missiles2.time2, numb_sec_reach_missile.time + missiles2.time2 FROM numb_sec_reach_missile, missiles2 WHERE numb_sec_reach_missile.missile_id = missiles2.missile_id"
        )

    # Convert the seconds of return_time.return.time to hh:mm:ss format
    # time stamp in following format : "2022-11-05 15:21:58.983496"
    # doing str(datetime.now())
    # id SERIAL PRIMARY KEY
    # missile_id INT
    # missiles_Intersects_middle geometry
    # distance DOUBLE PRECISION
    # time DOUBLE PRECISION
    # time2 DOUBLE PRECISION
    # return_time DOUBLE PRECISION
    # return_time_hh_mm_ss
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "DROP TABLE IF EXISTS return_time_hh_mm_ss;"
            "CREATE TABLE return_time_hh_mm_ss (id SERIAL PRIMARY KEY, missile_id INT, missiles_Intersects_middle geometry, distance DOUBLE PRECISION, time DOUBLE PRECISION, time2 DOUBLE PRECISION, return_time DOUBLE PRECISION, return_time_hh_mm_ss TIMESTAMP)"
        )
        cur.execute(
            "INSERT INTO return_time_hh_mm_ss (missile_id, missiles_Intersects_middle, distance, time, time2, return_time, return_time_hh_mm_ss) SELECT return_time.missile_id, return_time.missiles_Intersects_middle, return_time.distance, return_time.time, return_time.time2, return_time.return_time, now() + return_time.return_time * interval '3600 second' FROM return_time"
        )

    # make return_time_hh_mm_ss printable to json format
    # id SERIAL PRIMARY KEY
    # missile_id INT
    # missiles_Intersects_middle geometry
    # distance DOUBLE PRECISION
    # time DOUBLE PRECISION
    # time2 DOUBLE PRECISION
    # return_time DOUBLE PRECISION
    # return_time_hh_mm_ss
    # return_time_hh_mm_ss_printable string
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "DROP TABLE IF EXISTS return_time_hh_mm_ss_printable;"
            "CREATE TABLE return_time_hh_mm_ss_printable (id SERIAL PRIMARY KEY, missile_id INT, missiles_Intersects_middle geometry, distance DOUBLE PRECISION, time DOUBLE PRECISION, time2 DOUBLE PRECISION, return_time DOUBLE PRECISION, return_time_hh_mm_ss TIMESTAMP, return_time_hh_mm_ss_printable VARCHAR)"
        )
        cur.execute(
            "INSERT INTO return_time_hh_mm_ss_printable (missile_id, missiles_Intersects_middle, distance, time, time2, return_time, return_time_hh_mm_ss, return_time_hh_mm_ss_printable) SELECT return_time_hh_mm_ss.missile_id, return_time_hh_mm_ss.missiles_Intersects_middle, return_time_hh_mm_ss.distance, return_time_hh_mm_ss.time, return_time_hh_mm_ss.time2, return_time_hh_mm_ss.return_time, return_time_hh_mm_ss.return_time_hh_mm_ss, to_char(return_time_hh_mm_ss.return_time_hh_mm_ss, 'YYYY-MM-DD HH24:MI:SS') FROM return_time_hh_mm_ss"
        )



    # Change the return_time_hh_mm_ to CENTRAL TIME
    # id SERIAL PRIMARY KEY
    # missile_id INT
    # missiles_Intersects_middle geometry
    # distance DOUBLE PRECISION
    # time DOUBLE PRECISION
    # time2 DOUBLE PRECISION
    # return_time DOUBLE PRECISION
    # return_time_hh_mm_ss
    # return_time_hh_mm_ss_printable string
    # return_time_hh_mm_ss_printable_central_time
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "DROP TABLE IF EXISTS return_time_hh_mm_ss_printable_central_time;"
            "CREATE TABLE return_time_hh_mm_ss_printable_central_time (id SERIAL PRIMARY KEY, missile_id INT, missiles_Intersects_middle geometry, distance DOUBLE PRECISION, time DOUBLE PRECISION, time2 DOUBLE PRECISION, return_time DOUBLE PRECISION, return_time_hh_mm_ss TIMESTAMP, return_time_hh_mm_ss_printable VARCHAR, return_time_hh_mm_ss_printable_central_time VARCHAR)"
        )
        cur.execute(
            "INSERT INTO return_time_hh_mm_ss_printable_central_time (missile_id, missiles_Intersects_middle, distance, time, time2, return_time, return_time_hh_mm_ss, return_time_hh_mm_ss_printable, return_time_hh_mm_ss_printable_central_time) SELECT return_time_hh_mm_ss_printable.missile_id, return_time_hh_mm_ss_printable.missiles_Intersects_middle, return_time_hh_mm_ss_printable.distance, return_time_hh_mm_ss_printable.time, return_time_hh_mm_ss_printable.time2, return_time_hh_mm_ss_printable.return_time, return_time_hh_mm_ss_printable.return_time_hh_mm_ss, return_time_hh_mm_ss_printable.return_time_hh_mm_ss_printable, (return_time_hh_mm_ss_printable.return_time_hh_mm_ss_printable::timestamp + interval '6 hour')::text FROM return_time_hh_mm_ss_printable"
        )