from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse, HTMLResponse
import psycopg2
import json
import time
import requests
from re import S
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


url = "http://missilecommand.live:8080/FIRE_SOLUTION"

if __name__ == "__main__":
    
    # Create a solution.json that will have the following fields
    # "team_id" : teamID,
    #                     "target_missile_id": feature["id"],
    #                     "missile_type": MissileToSend[1],
    #                     "fired_time": FireTime,
    #                     "firedfrom_lat": battery["coordinates"][1],
    #                     "firedfrom_lon": battery["coordinates"][0],
    #                     "aim_lat": target[1],
    #                     "aim_lon": target[0],
    #                     "expected_hit_time": HitTime,
    #                     "target_alt": target[2]
    
    with DatabaseCursor(".config.json") as cur:
        cur.execute("SELECT * FROM team")
        teamID = cur.fetchone()[0]
        
        cur.execute("SELECT * FROM missile")
        missiles = cur.fetchall()
        
        cur.execute("SELECT * FROM battery")
        batteries = cur.fetchall()
        
        cur.execute("SELECT * FROM target")
        targets = cur.fetchall()
        
        cur.execute("SELECT * FROM target_missile")
        target_missiles = cur.fetchall()
        
        cur.execute("SELECT * FROM target_missile")
        target_missiles = cur.fetchall()
        
        cur.execute("SELECT * FROM target_missile")
        target_missiles = cur.fetchall()
        
        