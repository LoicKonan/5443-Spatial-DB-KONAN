from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse, HTMLResponse
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


"""
CREATE TABLE region (name text, geom geometry(multipolygon,4326));

CREATE TABLE arsenal ();

"""


def create_arsenal_table(name, insert_names, vals):
    name = str(name).replace("[", " ")
    name = name.replace("]", " ")
    name = name.replace("\'", " ")
    insert_names = str(insert_names).replace("[", " ")
    insert_names = insert_names.replace("]", " ")
    insert_names = insert_names.replace("\'", " ")
    vals = str(vals).replace("[", " ")
    vals = vals.replace("]", " ")

    create_arsenal = f"""
    CREATE TABLE arsenal ({names});
       
    """

    insert_value = f"""
    INSERT INTO arsenal ({insert_names})
    VALUES ({vals}) 
    """

    return create_arsenal, insert_value




if __name__ == "__main__":

    with open("region.json", "r") as f:
        data = json.loads(f.read())
        names = []
        insert_names = []
        vals = []
        id = data["id"]
        for key, value in data["arsenal"].items():
            names.append(key + " VARCHAR(128)")
            insert_names.append(key)
            vals.append(value)
            #print(key, value)

        for i in data["region"]["features"]:
            # print(i)
            geom = str(i["geometry"]).replace("\'", "\"")

        # print(geom)

        # print(names)
        sql = f"""
        INSERT INTO myregion (rid, geom)
        VALUES ({id}, ST_GeomFromGeoJSON('{geom}')) 
        
        """
        #create_arsenal_table(names, insert_names, vals)

        names = str(names).replace("[", " ")
        names = names.replace("]", " ")
        names = names.replace("\'", " ")
        insert_names = str(insert_names).replace("[", " ")
        insert_names = insert_names.replace("]", " ")
        insert_names = insert_names.replace("\'", " ")
        vals = str(vals).replace("[", " ")
        vals = vals.replace("]", " ")
        sql2 = f"""
        CREATE TABLE arsenal ({names});
        """

        sql3 = f"""
        INSERT INTO arsenal ({insert_names})
        VALUES ({vals}) 
        """
        print(sql3)
        print(sql2)
        with DatabaseCursor(".config.json") as cur:
            res = cur.execute(sql)
            answer = cur.fetchall()

            print(answer)
