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
import copy


"""
 
 ██████╗  █████╗ ████████╗ █████╗ ██████╗  █████╗ ███████╗███████╗
 ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝
 ██║  ██║███████║   ██║   ███████║██████╔╝███████║███████╗█████╗  
 ██║  ██║██╔══██║   ██║   ██╔══██║██╔══██╗██╔══██║╚════██║██╔══╝  
 ██████╔╝██║  ██║   ██║   ██║  ██║██████╔╝██║  ██║███████║███████╗
 ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝
                                                                  
  ██████╗██╗   ██╗██████╗ ███████╗ ██████╗ ██████╗                
 ██╔════╝██║   ██║██╔══██╗██╔════╝██╔═══██╗██╔══██╗               
 ██║     ██║   ██║██████╔╝███████╗██║   ██║██████╔╝               
 ██║     ██║   ██║██╔══██╗╚════██║██║   ██║██╔══██╗               
 ╚██████╗╚██████╔╝██║  ██║███████║╚██████╔╝██║  ██║               
  ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝               
                                                                  
 
    Creates an object that is used to connect to our postgres database
    and allows us to create tables and run queries directly connected to
    our Postgres database in pgAdmin.
"""

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
        
        
"""
    Needed to convert our timestamps to a format that the
    server would accept.
    
        - Example input time:  "2022-10-27 12:12:07"
        - Example return time: “25/05/99 19:42:50”
        
    - Byron
"""
def shouldHaveUsedUnixTimeStamps(timestamp):
    
    modified = (timestamp.replace(' ', '-')).split("-")
    
    year = modified[0][2::]
    
    return (modified[2] + '/' + modified[1] + '/' + year + ' ' + modified[3])


if __name__ == "__main__":
    
    """
        - Get all these information from the database and make a post send it to solution url
        - team_id           => get rid from myregion table
        - target_missile_id => Get the missile id from the table point_to_shoot
        - missile_type      => Get the missile type from the table speed database
        - fired_time        => Get the return time from the missile2 table.
        - firedfrom_lat     => Get the battery latitude from the table battery_lon_lat
        - firedfrom_lon     => Get the battery longitude from the table battery_lon_lat 
        - aim_lat           => Get the target latitude from the table point_to_shoot 
        - aim_lon           => Get the target latitude longitude from the table point_to_shoot
        - expected_hit_time => Get the return time from the return_time_hh_mm_ss table.
        - target_alt        => Get the target altitude from the table point_to_shoot_altitude
    """
    
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
        
    # Get the return time from the return_time_hh_mm_ss_printable_central_time table in string format.
    with DatabaseCursor(".config.json") as cur:
        cur.execute("SELECT return_time_hh_mm_ss_printable_central_time FROM return_time_hh_mm_ss_printable_central_time")
        return_time_hh_mm_ss_printable_central_time = cur.fetchall()
        # print
        print("return_time_hh_mm_ss_printable_central_time: ", return_time_hh_mm_ss_printable_central_time)
        
    # Get the target altitude from the table point_to_shoot_altitude
    with DatabaseCursor(".config.json") as cur:
        cur.execute("SELECT altitude FROM point_to_shoot_altitude")
        target_alt = cur.fetchall()
        # print
        print("target_alt: ", target_alt)
    
    
    
    """
 
    ██████╗ ███████╗████████╗██╗   ██╗██████╗ ███╗   ██╗
    ██╔══██╗██╔════╝╚══██╔══╝██║   ██║██╔══██╗████╗  ██║
    ██████╔╝█████╗     ██║   ██║   ██║██████╔╝██╔██╗ ██║
    ██╔══██╗██╔══╝     ██║   ██║   ██║██╔══██╗██║╚██╗██║
    ██║  ██║███████╗   ██║   ╚██████╔╝██║  ██║██║ ╚████║
    ╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝
                                                        
     ████████╗ ██████╗                                   
     ╚══██╔══╝██╔═══██╗                                  
        ██║   ██║   ██║                                  
        ██║   ██║   ██║                                  
        ██║   ╚██████╔╝                                  
        ╚═╝    ╚═════╝                                   
                                                        
    ███████╗███████╗███╗   ██╗██████╗ ███████╗██████╗   
    ██╔════╝██╔════╝████╗  ██║██╔══██╗██╔════╝██╔══██╗  
    ███████╗█████╗  ██╔██╗ ██║██║  ██║█████╗  ██████╔╝  
    ╚════██║██╔══╝  ██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗  
    ███████║███████╗██║ ╚████║██████╔╝███████╗██║  ██║  
    ╚══════╝╚══════╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝  
                                                     
 
"""
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
        "expected_hit_time": return_time_hh_mm_ss_printable_central_time,
        "target_alt": target_alt
    }
    
    team_id = 0
    MissileResponse1 = []

    MissileResponse = {
        "team_id": team_id,
        "target_missile_id": 0,
        "missile_type": "string",
        "fired_time": "string",
        "firedfrom_lat": 0,
        "firedfrom_lon": 0,
        "aim_lat": 0,
        "aim_lon": 0,
        "expected_hit_time": "string",
        "target_alt": 0
    }

    MissileFR = {
        "team_id": team_id,
        "target_missile_id": 0,
        "missile_type": "string",
        "fired_time": "string",
        "firedfrom_lat": 0,
        "firedfrom_lon": 0,
        "aim_lat": 0,
        "aim_lon": 0,
        "expected_hit_time": "string",
        "target_alt": 0
    }
    

    """
        This is where I dumped our JSON objects into a single list
        the way DeAngelo did it to get it to work
        
        - Byron
    """
    stupidList = []
    stupidList.append(solution)
    # send solution to the url and make a json file 
    with open("solution.json", "w") as f:
        json.dump(stupidList, f, indent=4)
        
    
    FinalMissiles = []

    with open("solution.json") as Fin:
        data = json.load(Fin)
        

    Fin.close()
    finalM = []

    for MR in data:
        ## Index Counter
        count = 0

        ## Number of missiles to read in 
        missileCount = len(MR["target_missile_id"])

        for i in range(0, missileCount):
            MissileFR["team_id"] = MR["team_id"][0][0]
            MissileFR["target_missile_id"] = MR["target_missile_id"][count][0]
            MissileFR["missile_type"] = MR["missile_type"][count][0]
            
            ## Getting the proper format timestamp
            HT = shouldHaveUsedUnixTimeStamps(MR["fired_time"][count][0])
            MissileFR["fired_time"] = HT
            
            MissileFR["firedfrom_lat"] = MR["firedfrom_lat"][0][0]
            MissileFR["firedfrom_lon"] = MR["firedfrom_lon"][0][0]
            MissileFR["aim_lat"] = MR["aim_lat"][count][0]
            MissileFR["aim_lon"] = MR["aim_lon"][count][0]
            
            ## Getting the proper format timestamp
            EHT = shouldHaveUsedUnixTimeStamps(MR["expected_hit_time"][count][0])
            MissileFR["expected_hit_time"] = EHT
            
            MissileFR["target_alt"] = MR["target_alt"][count][0]

            """
                Here is where the biggest change occurs
                
                Instead of messing with our file, we are sending them one at a time
                as we read them from the file.
                
                - Byron
            """
            finalM.append(copy.deepcopy(MissileFR))
            r = requests.post("http://missilecommand.live:8080/FIRE_SOLUTION/", json=MissileFR)
            print(r.text)
            
            count += 1



    ## Still writing the results for reference but don't really need it for calling the server
    ## - Byron
    with open ('responseMissiles.json', 'w') as Fout:

        json.dump(finalM, Fout, indent=4)

    Fout.close()



