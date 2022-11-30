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


url = "http://missilecommand.live:8080/REGISTER"

if __name__ == "__main__":
    
    # Register.
    while True:
        try:
            register = requests.get(url)
            with open('myregion.json', 'w') as f:
                json.dump(register.json(), f, indent=4)
                print(register.text)
            break
        except Exception:
            print("Connection error. Retrying in 5 seconds.")
            time.sleep(5)
            continue
    print("Registered with game server.")
    
    
    # Moving our data to the database
    with open("myregion.json", "r") as f:
        data = json.loads(f.read())
        names = []
        insert_names = []
        vals = []
        id = data["id"]
        for key, value in data["arsenal"].items():
            names.append(key + " VARCHAR(128)")
            insert_names.append(key)
            vals.append(value)
            # print(key, value)

        for i in data["region"]["features"]:
            # print(i)
            geom = str(i["geometry"]).replace("'", '"')

        # print(geom)
        print(names)

        # create the table myregion
        create_region = f"""
        DROP TABLE IF EXISTS myregion;
        CREATE TABLE myregion (rid integer, geom geometry(multipolygon,4326));
        alter table myregion add primary key (rid);
        """

        # insert the region
        sql = f"""
        INSERT INTO myregion (rid, geom)
        VALUES ({id}, ST_GeomFromGeoJSON('{geom}')) 
        
        """
        # print to see results
        print(sql)

        # create_arsenal_table(names, insert_names, vals)
        names = str(names).replace("[", " ")
        names = names.replace("]", " ")
        names = names.replace("'", " ")
        insert_names = str(insert_names).replace("[", " ")
        insert_names = insert_names.replace("]", " ")
        insert_names = insert_names.replace("'", " ")
        vals = str(vals).replace("[", " ")
        vals = vals.replace("]", " ")
        sql2 = f"""
        DROP TABLE IF EXISTS arsenal;
        CREATE TABLE arsenal ({names});
        """

        sql3 = f"""
        INSERT INTO arsenal ({insert_names})
        VALUES ({vals}) 
        """
        print(sql3)
        print(sql2)
        
        # print the 

        # insert myregion and arsenal to the database in postgresql
        with DatabaseCursor(".config.json") as cur:
            cur.execute(create_region)
            cur.execute(sql)
            cur.execute(sql2)
            cur.execute(sql3)
            cur.execute("SELECT * FROM myregion")
            print(cur.fetchall())
