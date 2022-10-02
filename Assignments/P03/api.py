"""
# Author      :     Loic Konan
# Title       :     Project 3 - Project 
# Date        :     09/29/2022 
# Description :
                    


"""


from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
import psycopg2
import json

"""
       
▄▀█ █▀█ █   █▀▀ █▀█ █▄░█ █▀▀ █ █▀▀ █░█ █▀█ ▄▀█ ▀█▀ █ █▀█ █▄░█   █ █▄░█ █▀▀ █▀█ █▀█ █▀▄▀█ ▄▀█ ▀█▀ █ █▀█ █▄░█
█▀█ █▀▀ █   █▄▄ █▄█ █░▀█ █▀░ █ █▄█ █▄█ █▀▄ █▀█ ░█░ █ █▄█ █░▀█   █ █░▀█ █▀░ █▄█ █▀▄ █░▀░█ █▀█ ░█░ █ █▄█ █░▀█


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
        #  
        self.cur = self.conn.cursor()
        self.cur.execute("SET search_path TO " + self.conn_config["schema"])

        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        # some logic to commit/rollback
        self.conn.commit()
        self.conn.close()



""" 
█▀▄ █▀▀ █▀ █▀▀ █▀█ █ █▀█ ▀█▀ █ █▀█ █▄░█
█▄▀ ██▄ ▄█ █▄▄ █▀▄ █ █▀▀ ░█░ █ █▄█ █░▀█
"""
description = """🚀 🅵🅰🆂🆃🅰🅿🅸 + 🅿🅾🆂🆃🅶🆁🅴🆂🆀🅻 🚀 """

app = FastAPI(
    title = "ⓁⓄⒾⒸ ⒶⓅⒾ ⓅⓇⓄⒿⒺⒸⓉ ⓪3",
    description = description,
    version = "0.0.1",
    contact = {
        "name": "𝐋𝐎𝐈𝐂 𝐊",
        "url": "https://www.linkedin.com/in/loickonan/",
    },
    license_info = {
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


""" 
                ▄▀█ █▀█ █   █▀█ █▀█ █░█ ▀█▀ █▀▀ █▀
                █▀█ █▀▀ █   █▀▄ █▄█ █▄█ ░█░ ██▄ ▄█
"""

# This api route is used to display the home page of the API.
@app.get("/")
async def docs_redirect():
    """
    ### Local api that has the following routes:\n
    
    -   findAll
    -   findOne
    -   findClosest
    
    """
    return RedirectResponse(url="/docs")





# This api routes is used to display the total number of AIRPORTS from a specific country.
@app.get("/Number of Airports in a Country")
async def airports2(country: str):
    """
    ### Display the total number of AIRPORTS from a specific country.
    
    """
    sql = f"""SELECT count(*) from airports2 
              WHERE country = '{country}'"""

    with DatabaseCursor(".config.json") as cur:
        cur.execute(sql)
        return cur.fetchone()
    









"""
            ░█▀▄▀█ ─█▀▀█ ▀█▀ ░█▄─░█ 
            ░█░█░█ ░█▄▄█ ░█─ ░█░█░█ 
            ░█──░█ ░█─░█ ▄█▄ ░█──▀█
"""

if __name__ == "__main__":
    uvicorn.run("api:app", port=8000, reload=True)