# import psycopg2
import json
import csv
import random

# The sign tells us whether we are north or south, east or west on the globe.
# A nonzero hundreds digit tells us we're using longitude, not latitude!
# The tens digit gives a position to about 1,000 kilometers. It gives us useful information about what continent or ocean we are on.
# The units digit (one decimal degree) gives a position up to 111 kilometers (60 nautical miles, about 69 miles). It can tell us roughly what large state or country we are in.
# The first decimal place is worth up to 11.1 km: it can distinguish the position of one large city from a neighboring large city.
# The second decimal place is worth up to 1.1 km: it can separate one village from the next.
# The third decimal place is worth up to 110 m: it can identify a large agricultural field or institutional campus.
# The fourth decimal place is worth up to 11 m: it can identify a parcel of land. It is comparable to the typical accuracy of an uncorrected GPS unit with no interference.
# The fifth decimal place is worth up to 1.1 m: it distinguish trees from each other. Accuracy to this level with commercial GPS units can only be achieved with differential correction.
# The sixth decimal place is worth up to 0.11 m: you can use this for laying out structures in detail, for designing landscapes, building roads. It should be more than good enough for tracking movements of glaciers and rivers. This can be achieved by taking painstaking measures with GPS, such as differentially corrected GPS.
# The seventh decimal place is worth up to 11 mm: this is good for much surveying and is near the limit of what GPS-based techniques can achieve.
# The eighth decimal place is worth up to 1.1 mm: this is good for charting motions of tectonic plates and movements of volcanoes. Permanent, corrected, constantly-running GPS base stations might be able to achieve this level of accuracy.
# The ninth decimal place is worth up to 110 microns: we are getting into the range of microscopy. For almost any conceivable application with earth positions, this is overkill and will be more precise than the accuracy of any surveying device.
# Ten or more decimal places indicates a computer or calculator was used and that no attention was paid to the fact that the extra decimals are useless. Be careful, because unless you are the one reading these numbers off the device, this can indicate low quality processing!


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


class DBQuery(object):
    def __init__(self, config):
        self.result = {}
        self.config = config
        self.limit = 1000
        self.offset = 0

    def __query(self, sql, qtype=3):
        with DatabaseCursor(self.config) as cur:
            print(sql)
            cur.execute(sql)

            if qtype == 1:
                self.result["data"] = cur.fetchone()
            elif qtype == 2:
                self.result["data"] = cur.fetchmany()
            else:
                self.result["data"] = cur.fetchall()

            self.result["limit"] = self.limit
            self.result["offset"] = self.offset
            self.result["sql"] = sql
            self.result["success"] = cur.rowcount > 0
            self.result["effectedRows"] = cur.rowcount
        return self.result

    def queryOne(self, sql, **kwargs):

        limit = kwargs.get("limit", self.limit)
        offset = kwargs.get("offset", self.offset)
        self.result["offset"] = offset

        if limit:
            self.limit = limit

        return self.__query(f"{sql} LIMIT {self.limit} OFFSET {offset}")

    def queryAll(self, sql, **kwargs):

        limit = kwargs.get("limit", self.limit)
        offset = kwargs.get("offset", self.offset)
        self.result["offset"] = offset

        if limit:
            self.limit = limit

        return self.__query(f"{sql} LIMIT {self.limit} OFFSET {offset}")

    def queryMany(self, sql, **kwargs):

        limit = kwargs.get("limit", self.limit)
        offset = kwargs.get("offset", self.offset)
        self.result["offset"] = offset

        if limit:
            self.limit = limit
        return self.__query(f"{sql} LIMIT {self.limit} OFFSET {offset}")


conn = DBQuery(".config.json")


StartAltitude = 10000
EndAltitude = 0


class RandTrajectory(object):
    def __init__(self, **kwargs):
        lon1 = kwargs.get("lon1", None)
        lat1 = kwargs.get("lat1", None)
        lon2 = kwargs.get("lon2", None)
        lat2 = kwargs.get("lat2", None)

    def getMilitaryBases(self):

        sql = "select * from us_mil;"

        with DatabaseCursor(".config.json") as cur:
            cur.execute(sql)
            return cur.fetchall()

    def getStartPointPG(self, side="South"):
        """Generates a random lon/lat on a predefined bounding box."""
        top = 54.3457868
        left = -129.7844079
        right = -61.9513812
        bottom = 19.7433195

        sides = {
            "North": [left, top, right, top],
            "South": [left, bottom, right, bottom],
            "East": [right, top, right, bottom],
            "West": [left, top, left, bottom],
        }
        sql = f"""SELECT ST_AsText(J.*) FROM (SELECT ST_GeneratePoints(geom, 1, 1996) 
        FROM (
        SELECT ST_Buffer(
            ST_GeomFromText('LINESTRING({sides[side][0]} {sides[side][1]},{sides[side][2]} {sides[side][3]})'),
        .5, 'endcap=round join=round')  As geom ) as s )as J;"""

        print(sql)

        # results = conn.queryAll(sql)
        # return results

    def getStartPoint(self, side="South"):
        """Generates a random lon/lat on a predefined bounding box."""
        top = 54.3457868
        left = -129.7844079
        right = -61.9513812
        bottom = 19.7433195

        xRange = abs(left) - abs(right)
        yRange = abs(top) - abs(bottom)

        if side in "North":
            return [-random.random() * xRange, top]
        if side in "South":
            return [-random.random() * xRange, bottom]
        if side in "East":
            return [right, random.random() * yRange]
        if side in "West":
            return [left, random.random() * yRange]


if __name__ == "__main__":
    RT = RandTrajectory()

    # print(RT.getMilitaryBases())
    directions = ["North", "South", "East", "West"]
    for i in range(100):
        random.shuffle(directions)
        print(f"{directions[0]} {RT.getStartPoint(directions[0])}")

