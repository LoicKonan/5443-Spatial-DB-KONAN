from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
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
        #  
        self.cur = self.conn.cursor()
        self.cur.execute("SET search_path TO " + self.conn_config["schema"])

        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        # some logic to commit/rollback
        self.conn.commit()
        self.conn.close()


description = """🚀 FastAPI + PostgreSQL """

app = FastAPI()

@app.get("/")
async def docs_redirect():
    """Api's base route that displays the information created above in the Api Info section."""
    return RedirectResponse(url="/docs")


@app.get("/airports2")
async def airports2():
    sql = "select * from airports2"

    with DatabaseCursor(".config.json") as cur:
        cur.execute(sql)
        return cur.fetchall()


@app.get("/airport/{country}")
async def airports2(country):
    sql = f"""SELECT * from airports2 
              WHERE country = '{country}'"""

    with DatabaseCursor(".config.json") as cur:
        cur.execute(sql)
        return cur.fetchall()


@app.get("/airportCount")
async def airports2(country: str):
    sql = f"""SELECT count(*) from airports2 
              WHERE country = '{country}'"""

    with DatabaseCursor(".config.json") as cur:
        cur.execute(sql)
        return cur.fetchone()


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)