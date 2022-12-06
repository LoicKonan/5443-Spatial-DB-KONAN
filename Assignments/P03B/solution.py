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


solution = "http://missilecommand.live:8080/FIRE_SOLUTION"

if __name__ == "__main__":
    
    # Get all these information from the database and make a post send it to solution url
    # team_id           => get rid from myregion table
    # target_missile_id => Get the missile id from the table point_to_shoot
    # missile_type      => Get the missile type from the table speed database
    # fired_time        => Get the return time from the missile2 table.
    # firedfrom_lat     => Get the battery latitude from the table battery_lon_lat
    # firedfrom_lon     => Get the battery longitude from the table battery_lon_lat 
    # aim_lat           => Get the target latitude from the table point_to_shoot 
    # aim_lon           => Get the target latitude longitude from the table point_to_shoot
    # expected_hit_time => Get the return time from the return_time_hh_mm_ss table.
    # target_alt        => Get the target altitude from the table point_to_shoot_altitude
    
    
    # Get the team id myregion table
    with DatabaseCursor(".config.json") as cur:
        cur.execute("SELECT rid FROM myregion")
        team_id = cur.fetchall()
        # print
        print("team_id: ", team_id)
        
    # Get the missile id from the table point_to_shoot
    with DatabaseCursor(".config.json") as cur:
        cur.execute("SELECT missile_id FROM point_to_shoot")
        missile_id = cur.fetchall()
        # print
        print("missile_id: ", missile_id)
        
    # Get the missile type from the table speed database
    with DatabaseCursor(".config.json") as cur:
        cur.execute("SELECT missile_type FROM speed")
        missile_type = cur.fetchall()
        # print
        print("missile_type: ", missile_type)
        
    # Get the return Fire time from the return_time_hh_mm_ss_printable table in string format.
    with DatabaseCursor(".config.json") as cur:
        cur.execute("SELECT return_time_hh_mm_ss_printable FROM return_time_hh_mm_ss_printable")
        return_time_hh_mm_ss_printable = cur.fetchall()
        # print
        print("return_time_hh_mm_ss_printable: ", return_time_hh_mm_ss_printable)
        
    # Get the battery latitude from the table battery_lon_lat
    with DatabaseCursor(".config.json") as cur:
        cur.execute("SELECT latitude FROM battery_lon_lat")
        battery_lat = cur.fetchall()
        # print
        print("battery_lat: ", battery_lat)
        
    # Get the battery longitude from the table battery_lon_lat
    with DatabaseCursor(".config.json") as cur:
        cur.execute("SELECT longitude FROM battery_lon_lat")
        battery_lon = cur.fetchall()
        # print
        print("battery_lon: ", battery_lon)
        
    # Get the target latitude from the table point_to_shoot
    with DatabaseCursor(".config.json") as cur:
        cur.execute("SELECT point_to_shoot_lat FROM point_to_shoot")
        point_to_shoot_lat = cur.fetchall()
        # print
        print("point_to_shoot_lat: ", point_to_shoot_lat)
        
    # Get the target latitude longitude from the table point_to_shoot
    with DatabaseCursor(".config.json") as cur:
        cur.execute("SELECT point_to_shoot_lon FROM point_to_shoot")
        point_to_shoot_lon = cur.fetchall()
        # print
        print("point_to_shoot_lon: ", point_to_shoot_lon)
        
    # Get the return time from the return_time_hh_mm_ss_printable table in string format.
    with DatabaseCursor(".config.json") as cur:
        cur.execute("SELECT return_time_hh_mm_ss_printable FROM return_time_hh_mm_ss_printable")
        return_time_hh_mm_ss_printable = cur.fetchall()
        # print
        print("return_time_hh_mm_ss_printable: ", return_time_hh_mm_ss_printable)
        
    # Get the target altitude from the table point_to_shoot_altitude
    with DatabaseCursor(".config.json") as cur:
        cur.execute("SELECT altitude FROM point_to_shoot_altitude")
        target_alt = cur.fetchall()
        # print
        print("target_alt: ", target_alt)
    
    # Create a solution.json that will have the following fields
    #                     "team_id" :"INT"
    #                     "missile_id": "INT"
    #                     "missile_type": "STRING"
    #                     "return_time_hh_mm_ss": "STRING"
    #                     "battery_lat": "INT"
    #                     "battery_lon": "INT"
    #                     "point_to_shoot_lat": "INT"
    #                     "point_to_shoot_lon": "INT"
    #                     "return_time_hh_mm_ss": "STRING";
    #                     "target_alt": "INT"
    
    
    # Make a solution.json that will have the results and send it to the solution url. 
    solution = {
        "team_id": team_id,
        "target_missile_id": missile_id,
        "missile_type": missile_type,
        "fired_time": return_time_hh_mm_ss_printable,
        "firedfrom_lat": battery_lat,
        "firedfrom_lon": battery_lon,
        "aim_lat": point_to_shoot_lat,
        "aim_lon": point_to_shoot_lon,
        "expected_hit_time": return_time_hh_mm_ss_printable,
        "target_alt": target_alt
    }
    
    # send solution to the url and make a json file 
    with open("solution.json", "w") as f:
        json.dump(solution, f)
        
    # send solution to the url
    url = "http://missilecommand.live:8080/FIRE_SOLUTION/"
    files = {'file': open('solution.json', 'rb')}
    r = requests.post(url, files=files)
    print(r.text)
    
    
    
    
    
        
    