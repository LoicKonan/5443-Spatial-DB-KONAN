import geojson
import json
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse,HTMLResponse 
import psycopg2
import json
from geojson import Point
import random
import itertools
from random import shuffle

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

table_sql = """
    DROP TABLE IF EXISTS public.ship2;
    CREATE TABLE public.ship2 (
    ship_id int,
    category text,
    shipclass text,
    displacement numeric,
    length numeric,
    width numeric,
    torpedolaunchers json,
    armament json,
    armor json,
    speed numeric,
    turn_radius numeric,
    geom GEOMETRY(POINT, 4326)
);
    """


cardinal_sql = """
    DROP TABLE IF EXISTS cardinal;
    CREATE TABLE cardinal (
    direction text, 
    start_degree numeric, 
    middle_degree numeric, 
    end_degree numeric
);
    """

with DatabaseCursor(".config.json") as cur:
    cur.execute(table_sql)
    #cur.execute(cardinal_sql)
        


ships = {}


#Get the upper and lower points of the given bounding box.
bbox = {
    "UpperLeft": {"lon": -10.31324002, "lat": 50.17116998},
    "LowerRight": {"lon": -8.06068579, "lat": 48.74631646},
}



degrees_start = random.uniform(0, 360)

#List of cardinal information mostly useless outside of randomly select a cardinal point
cardinalList = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
start_degree1 = [348.750, 11.250, 33.750, 56.250, 78.750, 101.250, 123.750, 146.250, 168.750, 191.250, 213.750, 236.250, 258.750, 281.250, 303.750, 326.250]


degrees = int(float(degrees_start))

index = int((degrees + 11.25) / 22.5)


#Randomly select bearings for each ship
type_cast = random.randint(0,15)
bearings = shuffle(start_degree1)
bearings = start_degree1[type_cast]

rand_direction = cardinalList[index % 16]

#Inserts the cardinal degree information into the table
with DatabaseCursor(".config.json") as cur:

    with open("cardinal.json", "r") as f:
        cardinal = json.load(f)
        for card in cardinal:
        
            sql = f"""
            INSERT INTO cardinal(direction, start_degree, middle_degree, end_degree)
            VALUES('{card["Direction"]}', {card["From d°"]}, {card["Middle d°"]}, {card["To d°"]})
            
            """
            #cur.execute(sql)



with DatabaseCursor(".config.json") as cur:

    #Make the bounding box and hold it as a polygon
    box = f"""SELECT ST_AsGeoJson(ST_AsText(ST_Envelope('POLYGON(
                    ({bbox['UpperLeft']['lon']} {bbox['UpperLeft']['lat']},
                    {bbox['UpperLeft']['lon']} {bbox["LowerRight"]['lat']},
                    {bbox['LowerRight']['lon']} {bbox["LowerRight"]['lat']},
                    {bbox['LowerRight']['lon']} {bbox['UpperLeft']['lat']},
                    {bbox['UpperLeft']['lon']} {bbox['UpperLeft']['lat']}
                    ))'::geometry)));"""
    
    cur.execute(box)
    box = cur.fetchall()[0][0]
    


    #ST_AsGeoJSON
    #Get center of the Bounding Box
    center_bbox = f"""SELECT ST_AsText(ST_Centroid('{box}'));"""
    
    cur.execute(center_bbox)
    center_point = cur.fetchall()[0][0]
    
    #Get the sector of the bouding box where ships will be deployed
    personal_region = f"""SELECT start_degree, middle_degree, end_degree FROM cardinal WHERE direction = '{rand_direction}'"""
    cur.execute(personal_region)
    answer = cur.fetchall()
    start = answer[0][0]
    end = answer[0][2]
 
    

    #Slice the bounding box
    spliced_bbox = f"""SELECT ST_AsGeoJSON(ST_AsText(ST_Split(
            '{box}'::geometry,
            ST_MakeLine(
                ST_MakeLine(ST_SetSRID(ST_Project('{center_point}'::geography, {200000}, RADIANS({start}))::geometry, 0), '{center_point}')::geometry,
                ST_MakeLine(ST_SetSRID(ST_Project('{center_point}'::geography, {200000}, RADIANS({end}))::geometry,0), '{center_point}')::geometry
                ))));"""


    
    cur.execute(spliced_bbox)
    spliced_bbox = cur.fetchall()[0][0]
    #print(spliced_bbox)

    #Sector where ships will be deployed
    sector = f"""SELECT ST_AsGeoJSON(ST_AsText(ST_GeometryN('{spliced_bbox}', 2)));"""
    #print(sector)
    cur.execute(sector)
    sector = cur.fetchall()[0][0]
   

    #Read in the ships from json file and insert them into the DB holding a counter of the number of ships
    with open("ships.json", "r") as f:        
        ships = json.loads(f.read())

        ship_count = 0
        for ship in ships:
            tor = json.dumps(ship["torpedoLaunchers"])
            armame = json.dumps(ship["armament"])
            arma = json.dumps(ship["armor"])

            sql = f"""
            INSERT INTO ship2 (ship_id, category, shipclass, length, width, torpedolaunchers, armament, armor, speed, turn_radius)
            VALUES ({ship["id"]}, '{ship["category"]}', '{ship["shipClass"]}', {ship["length"]}, {ship["width"]}, '{tor}', '{armame}', '{arma}', {ship["speed"]}, {ship["turn_radius"]}
            )
            """
            cur.execute(sql)
            ship_count += 1
    



    #generating random starting location inside of the spliced area. This is the first ship

    random_location_ship = f"""SELECT ST_AsGeoJSON(ST_AsText(ST_GeneratePoints('{sector}'::geometry, 1)));"""
    cur.execute(random_location_ship)
    random_location_ship = cur.fetchall()[0][0]
    
    random_location_ship= json.loads(random_location_ship)["coordinates"]
  
    random_location_ship = list(itertools.chain(*random_location_ship))

    random_ship_point = Point(random_location_ship)

    #Place starting ship point inside the bounding box
    first_wave = random_ship_point
    first_w = first_wave
    first_g = first_w
    og_one = first_g["coordinates"][0]
    og_two = first_g["coordinates"][1]

    #First ship placed as a point
    first_ship = f"""SELECT ST_AsGeoJSON(ST_MakePoint{og_one, og_two});
    """
    #print(test1)
    cur.execute(first_ship)
    maybe = cur.fetchall()[0][0]
    #print(maybe)
    
    #Hold a copy of the first ship longitude to add 0.0001 to move the position 222 m
    coord = first_w['coordinates'][1]
    coord_2 = first_w['coordinates'][1]
    coord_3 = first_w['coordinates'][1]
    
    
    coord = coord + 0.0001
    first_w['coordinates'][1] = coord
    one = first_w['coordinates'][0]
    two = first_w['coordinates'][1]
    #print(coord)


    second_wave = f"""SELECT ST_AsGeoJSON(ST_MakePoint{one, two});
    """
    #print(test1)
    cur.execute(second_wave)
    
    sec = cur.fetchall()[0][0]
    #print(sec)


    coord2 = coord_2 + 0.0002
    first_w['coordinates'][1] = coord2
    one = first_w['coordinates'][0]
    two = first_w['coordinates'][1]
    #print(coord2)

    third_wave = f"""SELECT ST_AsGeoJSON(ST_MakePoint{one, two});"""
    cur.execute(third_wave)
    
    thir = cur.fetchall()[0][0]
    #print(thir)


    coord3 = coord_3 + 0.0003
    first_w['coordinates'][1] = coord3
    one = first_w['coordinates'][0]
    two = first_w['coordinates'][1]
   

    fourth_wave = f"""SELECT ST_AsGeoJSON(ST_MakePoint{one, two});"""
    cur.execute(fourth_wave)
    
    four = cur.fetchall()[0][0]
  

    """SELECT ST_MakePoint(-71.1043443253471, 42.3150676015829);"""

    
   
    #Converting the string geojson output to json object
    
    first_temp = json.loads(maybe)
    #print(type(first_temp))
    second_w = json.loads(sec)
   
    thrid_w = json.loads(thir)

    fourth_w = json.loads(four)

 
    #Work on creating the staggering path for ships
    for i in range(0, ship_count):
        if i % 4 == 0: 
            #Adding 0.001 respectively to stragger the other ships in the fleet
            

            sec_coord = second_w['coordinates'][0]

            sec_coord = sec_coord - 0.001
            second_w['coordinates'][0] = sec_coord
            one = second_w['coordinates'][0]
            two = second_w['coordinates'][1]
            # sec_conversion = sec_conversion.replace("\'","\"")
            stagger = f"""
            SELECT ST_AsGeoJSON(ST_MakePoint{one, two});
            """
            cur.execute(stagger)
            answer = cur.fetchall()[0][0]
           

            add_second_location= json.loads(answer)["coordinates"]
            add_second_location = Point(add_second_location)

            adding2_location = f"""UPDATE ship2 SET geom = ST_GeomFromGeoJSON('{add_second_location}')  WHERE ship_id = {i};"""
            #print(adding_location)

            cur.execute(adding2_location)
            
        elif i % 4 == 1:
            #Adding 0.001 respectively to stragger the other ships in the fleet
            thr_coord = thrid_w['coordinates'][0]

            thr_coord = thr_coord - 0.001
            thrid_w['coordinates'][0] = thr_coord
            one = thrid_w['coordinates'][0]
            two = thrid_w['coordinates'][1]

            # sec_conversion = sec_conversion.replace("\'","\"")
            stagger = f"""
            SELECT ST_AsGeoJSON(ST_MakePoint{one, two});
            """
            cur.execute(stagger)
            answer = cur.fetchall()[0][0]
          

            add_third_location= json.loads(answer)["coordinates"]
            add_third_location = Point(add_third_location)

            adding3_location = f"""UPDATE ship2 SET geom = ST_GeomFromGeoJSON('{add_third_location}')  WHERE ship_id = {i};"""
            #print(adding_location)

            cur.execute(adding3_location)
        
        elif i % 4 == 2:
                #Adding 0.001 respectively to stragger the other ships in the fleet
                for_coord = fourth_w['coordinates'][0]

                for_coord = for_coord - 0.001
                fourth_w['coordinates'][0] = for_coord
                one = fourth_w['coordinates'][0]
                two = fourth_w['coordinates'][1]

                # sec_conversion = sec_conversion.replace("\'","\"")
                stagger = f"""
                SELECT ST_AsGeoJSON(ST_MakePoint{one, two});
                """
                cur.execute(stagger)
                answer = cur.fetchall()[0][0]
             

                add_fourth_location= json.loads(answer)["coordinates"]
                add_fourth_location = Point(add_fourth_location)

                adding4_location = f"""UPDATE ship2 SET geom = ST_GeomFromGeoJSON('{add_fourth_location}')  WHERE ship_id = {i};"""
                #print(adding_location)

                cur.execute(adding4_location)
        
        else:
            #Adding 0.001 respectively to stragger the other ships in the fleet
            first_coord = first_temp['coordinates'][0]

            first_coord = first_coord - 0.001
            first_temp['coordinates'][0] = first_coord
            one = first_temp['coordinates'][0]
            two = first_temp['coordinates'][1]

            # sec_conversion = sec_conversion.replace("\'",W"\"")
            stagger = f"""
                SELECT ST_AsGeoJSON(ST_MakePoint{one, two});
                """
            cur.execute(stagger)
            answer = cur.fetchall()[0][0]
           

            add_first_location= json.loads(answer)["coordinates"]
            add_first_location = Point(add_first_location)

            adding1_location = f"""UPDATE ship2 SET geom = ST_GeomFromGeoJSON('{add_first_location}')  WHERE ship_id = {i};"""
            #print(adding_location)

            cur.execute(adding1_location)

            




    #Create final json object
    final_product = {
        "fleet_id": "Poseidon",
        "ship_status": []
    }

    final_sql = "SELECT ship_id, ST_asGeoJSON(geom) FROM ship2"
    cur.execute(final_sql)
    #print(final_sql)
    answers = cur.fetchall()
    #print(answers)

    for answer in answers:
        final_product["ship_status"].append({"ship_id": answer[0], "bearing": bearings, "location": {"latitude": json.loads(answer[1])["coordinates"][0], "longitude":json.loads(answer[1])["coordinates"][1]}})

    #Prints results to json file
    with open("final_product.json", "w") as file:
        json.dump(final_product, file, indent=4)
    


    

if __name__ == "__main__":

    pass



