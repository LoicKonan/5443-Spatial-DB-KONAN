from datetime import datetime
import json
from operator import truediv
from fastapi import FastAPI
import time
import requests
import uvicorn
import psycopg2
import pprint as pp


app = FastAPI()

url = "http://missilecommand.live:8080/RADAR_SWEEP"

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

def get_sec(time_str):
    """Get seconds from time."""
    h, m, s = time_str.split(':')
    return (int(h) * 3600 + int(m) * 60 + int(s))


def radar_sweep():
    while(True):
        
        time.sleep(3.5)

        with open("temp.json", "w") as f:
            register_region = requests.get(url)
            json.dump(register_region.json(), f, indent=4)
        

        with open("temp.json", "r") as f:
            data = json.loads(f.read())
            count = 0
            for i in data["features"]:
            
                mid = i["id"]
                longitue = i["geometry"]["coordinates"][0]
                latitude = i["geometry"]["coordinates"][1]
                bearing = i["properties"]["bearing"]
                altitude = i["properties"]["altitude"]
                currents_time = get_sec(i["properties"]["current_time"])
                #test = i["properties"]["missile_type"]

                sql = f"""INSERT INTO sweep(mid, Latitude, Longitude, bearing, altitude, currents_time) VALUES ({mid},{longitue}, {latitude}, {bearing}, {altitude}, {currents_time});
                
                """

                count+=1
                with DatabaseCursor(".config.json") as cur:
                    cur.execute(sql)
                    #answer = cur.fetchall()
        


        #print(r.text)

def current_time():
    return get_sec(datetime.now())


##############################################

def change_in_time():
    sys_time = current_time()
    calculation = sys_time - x
    return calculation



def interpolation_point(lon1: float = -98.48, lat1: float = 19.88, altitude1: float =  10000, lon2: float = -95.93, lat2: float = 36.14,   altitude2: int = 0):
    sql = f"""
     SELECT ST_AsText(ST_LineInterpolatePoints('LINESTRING({lon1} {lat1} {altitude1}, {lon2} {lat2} {altitude2})', 0.01)); 
    
    """
    with DatabaseCursor(".config.json") as cur:
        cur.execute(sql)
        answer = cur.fetchall()

    return answer
    

def speed():
    pass

def distance():
    sql = """
    select ST_distance(St_MakePoint(-98.48, 19.88, 10000)::geography,ST_MakePoint( -95.93, 36.14, 0)::geography);
    
    """

    with DatabaseCursor(".config.json") as cur:
        cur.execute(sql)
        answer = cur.fetchall()

    return answer


"""
Drop exisiting
Create a table with the values from the radar sweep
Update Table

"""

drop_table = "DROP TABLE  IF EXISTS radar_sweep;"

create_table = """

CREATE TABLE radar_sweep (
  
  id int NOT NULL,
  Latitude float ,
  Longitude float,
  bearing float,
  altitude float,
  currents_time float,
  geom GEOMETRY(POINT, 4326),
  CONSTRAINT radar_sweep_pkey PRIMARY KEY (id)
);

UPDATE radar_sweep
SET location = ST_SetSRID(ST_MakePoint(Longitude,Latitude), 4326);

"""



if __name__ == "__main__":
    radar_sweep()
   