from fastapi import FastAPI
from pydantic import BaseModel  # to create class models
from fastapi.responses import RedirectResponse
import uvicorn
import psycopg2
import json
import random
from math import radians, degrees, cos, sin, asin, sqrt, pow, atan2

import time



from module import DatabaseCursor
from module import DBQuery

class MissileSol(BaseModel):
    id:  str   # id of group
    time: int   # Time launched
    mid: int   # Missile Type
    lon1: float # starting X
    lat1: float # starting Y
    alt1: float # starting Z
    lon2: float # target X
    lat2: float # target Y
    alt2: float # target Z

app = FastAPI()


conn = DBQuery(".config.json")


"""
  _____   ____  _    _ _______ ______  _____
 |  __ \ / __ \| |  | |__   __|  ____|/ ____|
 | |__) | |  | | |  | |  | |  | |__  | (___
 |  _  /| |  | | |  | |  | |  |  __|  \___ \
 | | \ \| |__| | |__| |  | |  | |____ ____) |
 |_|  \_\\____/ \____/   |_|  |______|_____/
"""


@app.get("/")
async def docs_redirect():
    """Api's base route that displays the information created above in the ApiInfo section."""
    return RedirectResponse(url="/docs")

@app.get("/missileNext")
def missileNext(lon:float=-98.12345, lat:float=34.2345, speed:float=333, bearing:float=270, time:int=1, drop:float=0.0 , geojson:bool=False):
    """
    lon (float) : x coordinate
    lat (float) : y coordinate
    speed (int) : meters per second
    bearing (float) : direction in degrees (0-360)
    """
    if not geojson:
        select = "lon1 as x1, lat1 as y1, st_x(p2) as x2,st_y(p2) as y2"
    else:
        select = "ST_AsGeoJSON(p2)"

    sql = f"""
    WITH 
        Q1 AS (
            SELECT {lon} as lon1,{lat} as lat1, ST_SetSRID(ST_Project('POINT({lon} {lat})'::geometry, {speed*time}, radians({bearing}))::geometry,4326) as p2
        )
 
    SELECT {select}
    FROM Q1
    """

    print(sql)

    res = conn.queryOne(sql)

    cleanResult = {
        "lon1":res['data'][0],
        "lat1":res['data'][1],
        "lon2":res['data'][2],
        "lat2":res['data'][3]
    }

    res['data'] = cleanResult

    return res


@app.get("/missile_path")
def missilePath(d: str = None, buffer: float = 0):
    """ Returns a missile path across the entire continental US 
        **Not sure how necessary this is:)**
    ### Params:
        d (str) : direction of missile, if None then it will be random
        buffer (float) : a padding added to or from the bbox (Cont US)
    ### Returns:
        [float,float] start and end
    """
    bbox = {
        "l": -124.7844079,  # left
        "r": -66.9513812,  # right
        "t": 49.3457868,  # top
        "b": 24.7433195,  # bottom
    }

    directions = ["N", "S", "E", "W"]

    if not d:
        d = random.shuffle(directions)

    x1 = ((abs(bbox["l"]) - abs(bbox["r"])) * random.random() + abs(bbox["r"])) * -1
    x2 = ((abs(bbox["l"]) - abs(bbox["r"])) * random.random() + abs(bbox["r"])) * -1
    y1 = (abs(bbox["t"]) - abs(bbox["b"])) * random.random() + abs(bbox["b"])
    y2 = (abs(bbox["t"]) - abs(bbox["b"])) * random.random() + abs(bbox["b"])

    if d == "N":
        start = [x1, bbox["b"] - buffer]
        end = [x2, bbox["t"] + buffer]
    elif d == "S":
        start = [x1, bbox["t"] + buffer]
        end = [x2, bbox["b"] - buffer]
    elif d == "E":
        start = [bbox["l"] - buffer, y1]
        end = [bbox["r"] + buffer, y2]
    else:
        start = [bbox["r"] + buffer, y1]
        end = [bbox["l"] - buffer, y2]

    return [start, end]


@app.get("/getArsenal")
def getArsenal(id: str = None, total: int = 50):
    """Returns a missile arsenal randomly generated weighted to
        give more slower weaker missiles that fast and strong.
    Params:
        id (str) : id of the team
        total (int) : total number of missiles to be issued
    """
    # names = list(missile_data["missiles"].keys())

    # missiles = []

    # i = len(names)*2
    # for name in sorted(names):
    #     print(name,i)
    #     missiles.extend([name] * i)
    #     print(len(missiles))
    #     i -= 2

    # random.shuffle(missiles)

    # missileCount = {}

    # sum = 0
    # for name in names:
    #     missileCount[name] = missiles[:total].count(name)

    #     if missileCount[name] == 0:
    #         missileCount[name] += 1
    #         missileCount["Atlas"] -= 1

    #     sum += missileCount[name]

    # missileCount['total'] = sum
    # return missileCount
    pass


@app.get("/radar_sweep")
def radar_sweep(gid:str):
    sql = """SELECT * FROM missile_attacking 
    WHERE gid like '{gid}'
    ORDER BY time
    """
    #res = conn.queryMany(sql)

    print(time.time())

    return {"hello":gid,"time":time.time()}


@app.get("/numRegions")
def region():
    sql = "SELECT distinct(gid) FROM regions ORDER BY gid"
    res = conn.queryMany(sql)

    return res


@app.get("/region")
def region(gid: int, cid: int):
    """ Returns a region geojson based on the gid and cid passed in.
    ### Params:
        gid (int) : This is the group id where 4 = four regions up to 8 for eight regions.
        cid (int) : This is a value `0-(gid-1)` numbering the region.
    ### Returns:
        (geojson) : polygon or multipolygon representing the region
    """

    # if cid >= gid:
    #     return {"Error": f"cid must be between 0 and {gid-1} for a gid of {gid}!"}


    sql = f"""
    SELECT geom::json as region FROM public.regions_simple 
    WHERE gid = {gid} AND cid = {cid}
    """

    res = conn.queryOne(sql, noPagination=True)

    # print(type(res['data']))
    # print(len(res['data']))
    # if isinstance(res['data'], list):
    #     with open('zzz2.json','w') as f:
    #         json.dump(res['data'][0][0],f,indent=4)

    fc = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": res["data"][0][0]["type"],
                    "coordinates": res["data"][0][0]["coordinates"],
                },
            }
        ],
    }

    return fc


@app.get("/missileInfo")
def missileInfo(name: str = None):
    """Get the speed and blast radius for the arsenal of missiles.
    ### Params:
        name (str) : filter the results to match name. Otherwise all missiles are returned.
    ### Returns:
        (list) : one or all missiles
    """

    where = ""

    if name:
        where = f"WHERE missile.name like '{name}'"

    sql = f"""
        SELECT
        missile.name,
        missile_speed.ms,
        missile_blast.blast_radius
        FROM
        missile
        INNER JOIN missile_speed ON missile.speed_cat = missile_speed.cat
        INNER JOIN missile_blast ON missile.blast_cat = missile_blast.cat
        {where}
    """

    print(sql)

    res = conn.queryMany(sql)

    returnVals = []

    for row in res['data']:
        returnVals.append({"name":row[0],"speed":row[1],"blast":row[2]})

    return returnVals


@app.get("/missileSolution/")
async def getSolution(id:str):
    sql = f"SELECT * FROM public.missile_solution WHERE id like '{id}'"
    res = conn.queryMany(sql)
    return res

@app.post("/missileSolution/")
async def postSolution(ms: MissileSol):

# {
#   "id": "string",
#   "time": 1010101,
#   "mid": 2,
#   "lon1": 11,
#   "lat1": 22,
#   "alt1": 1000,
#   "lon2": 33,
#   "lat2": 44,
#   "alt2": 1000
# }

    sql = f"""INSERT INTO public.missile_solution(
        id, "time", mid, lon1, lat1, alt1, lon2, lat2, alt2)
        VALUES ('{ms.id}', {ms.time}, {ms.mid}, {ms.lon1}, 
        {ms.lat1}, {ms.alt1}, {ms.lon2}, {ms.lat2}, {ms.alt2});"""

    res = conn.queryPost(sql)
    return res

"""
This main block gets run when you invoke this file. How do you invoke this file?
        python api.py 
After it is running, copy paste this into a browser: http://127.0.0.1:8080 
You should see your api's base route!
Note:
    Notice the first param below: api:app 
    The left side (api) is the name of this file (api.py without the extension)
    The right side (app) is the bearingiable name of the FastApi instance declared at the top of the file.
"""
if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8181, log_level="debug", reload=True)