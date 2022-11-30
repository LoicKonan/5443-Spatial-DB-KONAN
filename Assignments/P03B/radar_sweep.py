import time
import requests
import json
from re import S
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
import psycopg2
import json


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

if __name__ == '__main__':

    # Using that while loop to send a request to the sweep and send the missiles to missiles1.json
    # then after 3 more seconds send to missiles2.json, then stop.
    while True:
        response = requests.get(sweep)
        # print(response.text)
        with open('missile1.json', 'w') as f:
            json.dump(response.json(), f, indent=4)

        time.sleep(3)
        response = requests.get(sweep)
        # print(response.text)
        with open('missile2.json', 'w') as f:
            json.dump(response.json(), f, indent=4)
        break

    # Here I'm changing the current_time in missile1.json to number of seconds then save it as double precision.
    with open('missile1.json') as f:
        data = json.load(f)
        for i in data['features']:
            i['properties']['current_time'] = int(i['properties']['current_time'][:2]) * 3600 + int(
                i['properties']['current_time'][3:5]) * 60 + int(i['properties']['current_time'][6:8])
            # print(i['properties']['current_time'])

        # Here I'm updating the current_time to the new time in the missile1.json
        with open('missile1.json', 'w') as f:
            json.dump(data, f, indent=4)

    # Here I'm changing the current_time in missile1.json to number of seconds then save it as double precision.
    with open('missile2.json') as f:
        data = json.load(f)
        for i in data['features']:
            i['properties']['current_time'] = int(i['properties']['current_time'][:2]) * 3600 + int(
                i['properties']['current_time'][3:5]) * 60 + int(i['properties']['current_time'][6:8])
            # print(i['properties']['current_time'])

        # Here I'm updating the current_time to the new time in missile1.json
        with open('missile2.json', 'w') as f:
            json.dump(data, f, indent=4)

    # Here I'm creating a table called missiles1 from missiles1.json then load it with the data from missile1.json
    # then load it to the database.
    # id is a primary key int
    # missile id int
    # latitude double precision
    # longitude double precision
    # bearing double precision
    # altitude double precision
    # current_time int
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "DROP TABLE IF EXISTS missiles1;"
            "CREATE TABLE missiles1 (id SERIAL PRIMARY KEY, missile_id INT, latitude DOUBLE PRECISION, longitude DOUBLE PRECISION, bearing DOUBLE PRECISION, altitude DOUBLE PRECISION, time1 DOUBLE PRECISION)"
        )
        with open('missile1.json') as f:
            data = json.load(f)
            for i in data['features']:
                cur.execute(
                    "INSERT INTO missiles1 (missile_id, latitude, longitude, bearing, altitude, time1) VALUES (%s, %s, %s, %s, %s, %s)",
                    (i['id'], i['geometry']['coordinates'][1], i['geometry']['coordinates'][0], i['properties']['bearing'],
                     i['properties']['altitude'], i['properties']['current_time']))

    print("Incoming missiles1 loaded to database.")

    # Here I'm creating a table called missiles2 from missiles2.json then load it with the data from missile2.json
    # then load it to the database.
    # id is a primary key int
    # missile id int
    # latitude double precision
    # longitude double precision
    # bearing double precision
    # altitude double precision
    # current_time int
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "DROP TABLE IF EXISTS missiles2;"
            "CREATE TABLE missiles2 (id SERIAL PRIMARY KEY, missile_id INT, latitude DOUBLE PRECISION, longitude DOUBLE PRECISION, bearing DOUBLE PRECISION, altitude DOUBLE PRECISION, time2 DOUBLE PRECISION)"
        )
        with open('missile2.json') as f:
            data = json.load(f)
            for i in data['features']:
                cur.execute(
                    "INSERT INTO missiles2 (missile_id, latitude, longitude, bearing, altitude, time2) VALUES (%s, %s, %s, %s, %s, %s)",
                    (i['id'], i['geometry']['coordinates'][1], i['geometry']['coordinates'][0], i['properties']['bearing'],
                        i['properties']['altitude'], i['properties']['current_time']))

    print("Incoming missiles2 loaded to database.")


    # drop rate = abs(change in alt / change in time)
    # Find the the absolute value of the drop_rate between missile1 and missile2
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "SELECT missiles1.missile_id, missiles1.latitude, missiles1.longitude, missiles1.bearing, missiles1.altitude, missiles1.time1, missiles2.altitude, missiles2.time2, ABS((missiles2.altitude - missiles1.altitude) / (missiles2.time2 - missiles1.time1)) AS drop_rate FROM missiles1 INNER JOIN missiles2 ON missiles1.missile_id = missiles2.missile_id"
        )
        for row in cur.fetchall():
            print(row)
            
    print("Drop Rate Table Loaded to database.")
            
    # Here I'm creating a table called drop_rate from the drop_rate between missile1 and missile2
    # then load it to the database.
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

    # how many seconds until it hit the ground = abs (alt / drop rate)
    # Find the time until the missile hits the ground
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "SELECT missile_id, latitude, longitude, bearing, altitude, time1, altitude2, time2, drop_rate, ABS(altitude / drop_rate) AS time_to_hit_ground FROM drop_rate"
        )
        for row in cur.fetchall():
            print(row)
    print("Time to hit ground TABLE loaded to database.")
            
    # Here I'm creating a table called time_to_hit_ground from the time until the missile hits the ground
    # then load it to the database.
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
            "CREATE TABLE time_to_hit_ground (id SERIAL PRIMARY KEY, missile_id INT, latitude DOUBLE PRECISION, longitude DOUBLE PRECISION, bearing DOUBLE PRECISION, altitude DOUBLE PRECISION, time1 DOUBLE PRECISION, altitude2 DOUBLE PRECISION, time2 DOUBLE PRECISION, drop_rate DOUBLE PRECISION, time_to_hit_ground DOUBLE PRECISION)"
        )
        cur.execute(
            "INSERT INTO time_to_hit_ground (missile_id, latitude, longitude, bearing, altitude, time1, altitude2, time2, drop_rate, time_to_hit_ground) SELECT missile_id, latitude, longitude, bearing, altitude, time1, altitude2, time2, drop_rate, ABS(altitude / drop_rate) AS time_to_hit_ground FROM drop_rate"
        )


    # Find the speed of the missile
    with DatabaseCursor(".config.json") as cur:
        cur.execute(
            "SELECT missile_id, latitude, longitude, bearing, altitude, time1, altitude2, time2, drop_rate, time_to_hit_ground, ST_Distance(ST_MakePoint(longitude, latitude), ST_MakePoint(longitude, latitude)) / (time2 - time1) AS speed FROM time_to_hit_ground"
        )
        for row in cur.fetchall():
            print(row)
    print("Speed TABLE loaded to database.")
    
    # Here I'm creating a table called speed from the speed of the missile
    # then load it to the database.
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
            "CREATE TABLE speed (id SERIAL PRIMARY KEY, missile_id INT, latitude DOUBLE PRECISION, longitude DOUBLE PRECISION, bearing DOUBLE PRECISION, altitude DOUBLE PRECISION, time1 DOUBLE PRECISION, altitude2 DOUBLE PRECISION, time2 DOUBLE PRECISION, drop_rate DOUBLE PRECISION, time_to_hit_ground DOUBLE PRECISION, speed DOUBLE PRECISION)"
        )
        cur.execute(
            "INSERT INTO speed (missile_id, latitude, longitude, bearing, altitude, time1, altitude2, time2, drop_rate, time_to_hit_ground, speed) SELECT missile_id, latitude, longitude, bearing, altitude, time1, altitude2, time2, drop_rate, time_to_hit_ground, ST_Distance(ST_MakePoint(longitude, latitude), ST_MakePoint(longitude, latitude)) / (time2 - time1) AS speed FROM time_to_hit_ground"
        )
        

    # uses postgis project to get the exact location that the missile will reach alt = 0

    # uses postgis contains to check if the hit point is in the polygon

    # makes it so that perceived hit point is actually the city it is most likely targeting

    # if the hit point is in the polygon then the do the algo

    # uses postgis to get a set of (100) points along the line with the missile for interception

    # used to print the missiles path for visualization purposes not needed!!!
    #print('{"type": "Feature", "properties": {}, "geometry":' + str(MissileLineWithPoints) + "},")

    # the point we want to try and intercept (halfway point)

    # gets the closest battery to where we want to intercept

    # makes 3d point at alt 0

    # use drop rate and altitude of at target location to get time at target location

    # gets the distance from the battery to the missile in meters

    # the minimum speed of a missile to reach the target

    # gets the info of the missile to shoot

    # decrements the missile used

    # #gets the amount of seconds needed to reach target with given missile

    # gets when we need to fire from battery

    # gets the timestamp we need to fire from battery

    # gets hit time in required way
