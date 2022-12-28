import math
import json
import random

PI = math.pi

missile_dict = {
    "Atlas": {"speed": 1, "blast": 7},
    "Harpoon": {"speed": 2, "blast": 8},
    "Hellfire": {"speed": 3, "blast": 7},
    "Javelin": {"speed": 4, "blast": 7},
    "Minuteman": {"speed": 5, "blast": 9},
    "Patriot": {"speed": 6, "blast": 6},
    "Peacekeeper": {"speed": 7, "blast": 6},
    "SeaSparrow": {"speed": 8, "blast": 5},
    "Titan": {"speed": 8, "blast": 5},
    "Tomahawk": {"speed": 9, "blast": 6},
    "Trident": {"speed": 9, "blast": 9},
}

speed_dict = {
    1: {"ms": 111, "mph": 248.307},
    2: {"ms": 222, "mph": 496.614},
    3: {"ms": 333, "mph": 744.921},
    4: {"ms": 444, "mph": 993.228},
    5: {"ms": 555, "mph": 1241.535},
    6: {"ms": 666, "mph": 1489.842},
    7: {"ms": 777, "mph": 1738.149},
    8: {"ms": 888, "mph": 1986.456},
    9: {"ms": 999, "mph": 2234.763},
}

blast_dict = {1: 200, 2: 300, 3: 400, 4: 500, 5: 600, 6: 700, 7: 800, 8: 900, 9: 1000}


def missileStats(name):
    data = missile_dict[name]
    speed = speed_dict[data["speed"]]
    blast = blast_dict[data["blast"]]
    return {"speed": speed, "blast": blast}


# | decimals | degrees    | distance |
# | :------: | :--------- | -------: |
# |    0     | 1.0        |   111 km |
# |    1     | 0.1        |  11.1 km |
# |    2     | 0.01       |  1.11 km |
# |    3     | 0.001      |    111 m |
# |    4     | 0.0001     |   11.1 m |
# |    5     | 0.00001    |   1.11 m |
# |    6     | 0.000001   |  0.111 m |
# |    7     | 0.0000001  |  1.11 cm |
# |    8     | 0.00000001 |  1.11 mm |


def mph(metersPerSecond):
    return 2.237 * metersPerSecond


def dropRate(speed, distance, altitude):
    time = distance / speed

    return {"time": time, "rate": altitude / time}


def getRandomPointOnBBox(d=None, buffer=0):
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


def calcPosition(lon, lat, speed, angle, time=1, geojson=False):
    """
    lon (float) : x coordinate
    lat (float) : y coordinate
    speed (int) : meters per second
    angle (float) : direction in degrees (0-360)
    multiline(bool) : return the next position as point or interpolated line
    """
    if not geojson:
        select = "st_x(p2) as x,st_y(p2) as y"
    else:
        select = "ST_AsGeoJSON(p2)"

    sql = f"""
    WITH 
        Q1 AS (
            SELECT ST_SetSRID(ST_Project('POINT({lon} {lat})'::geometry, {speed*time}, radians({angle}))::geometry,4326) as p2
        )
 
    SELECT {select}
    FROM Q1
    """

    print(sql)


class Missile:
    def __init__(self):
        self.speed = 555  # speed in m/s
        self.blastRadius = 500  # radius in meters
        self.lon = -98.0  # x coord
        self.lat = 34.0  # y coord
        self.alt = 0.0  # z coord (altitude)

    def move(self, dx, dy, dz):
        self.lon += dx
        self.lat += dy
        self.alt += dz


if __name__ == "__main__":
    calcPosition(-98, 34, 1110, 270, 60, True)
    print(getRandomPointOnBBox("N", 10))
    print(getRandomPointOnBBox("E", 7))
    stats = missileStats("Patriot")

    print(stats)
    print(dropRate(stats["speed"]["ms"], 3054929, 13000))