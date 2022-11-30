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


url = "http://missilecommand.live:8080/RADAR_SWEEP"

if __name__ == '__main__':

    # Using that while loop to send a request to the url and send the missiles to missiles1.json 
    # then after 3 more seconds send to missiles2.json, then stop.
    while True:
        response = requests.get(url)
        # print(response.text)
        with open('missile1.json', 'w') as f:
            json.dump(response.json(), f, indent = 4)

        time.sleep(3)
        response = requests.get(url)
        # print(response.text)
        with open('missile2.json', 'w') as f:
            json.dump(response.json(), f, indent = 4)
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
            json.dump(data, f, indent = 4)

    # Here I'm changing the current_time in missile1.json to number of seconds then save it as double precision.
    with open('missile2.json') as f:
        data = json.load(f)
        for i in data['features']:
            i['properties']['current_time'] = int(i['properties']['current_time'][:2]) * 3600 + int(
                i['properties']['current_time'][3:5]) * 60 + int(i['properties']['current_time'][6:8])
            # print(i['properties']['current_time'])

        # Here I'm updating the current_time to the new time in missile1.json
        with open('missile2.json', 'w') as f:
            json.dump(data, f, indent = 4)
            

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

