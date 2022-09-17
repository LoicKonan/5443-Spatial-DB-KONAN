"""
# Author      :     Loic Konan
# Title       :     Project 2A - World Data setup with Postgres + Postgis + Fastapi + Docker
# Date        :     09/08/2022 
# Description :
                    Postgres + Postgis + Fastapi + Docker.
                    Using Pgadmin4 for Visualization tools to help debug problems.
                    Created a DataBase called Project1 with a public schema.
                    The table creation is done in the Pgadmin4.
                    Created a table called "airports" with the following columns:
                        - id
                        - name
                        - city
                        - country
                        - three_code
                        - four_code
                        - lat (latitude)
                        - lon (longitude)
                        - elevation 
                        - gmt 
                        - tz (timezone)
                        - timezone
                        - type 
                        - location (spatial geometry)
                        
                    Created a **location** column with a geometry data type for spatial query's to be run.
                    Created a local database using data files located at the following address: 
                    <https://cs.msutexas.edu/~griffin/data/> (Airports).
                    Created GET routes to retrieve data from the database using the following route:
                    <http://127.0.0.1:8000/docs#/> (Swagger).


"""


from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
import psycopg2
import json

"""
       
▄▀█ █▀█ █   █▀▀ █▀█ █▄░█ █▀▀ █ █▀▀ █░█ █▀█ ▄▀█ ▀█▀ █ █▀█ █▄░█   █ █▄░█ █▀▀ █▀█ █▀█ █▀▄▀█ ▄▀█ ▀█▀ █ █▀█ █▄░█
█▀█ █▀▀ █   █▄▄ █▄█ █░▀█ █▀░ █ █▄█ █▄█ █▀▄ █▀█ ░█░ █ █▄█ █░▀█   █ █░▀█ █▀░ █▄█ █▀▄ █░▀░█ █▀█ ░█░ █ █▄█ █░▀█


            Making a simple API with FastAPI and PostgreSQL
            Connect to the database and get the data
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
    title = "ⓁⓄⒾⒸ ⒶⓅⒾ ⓅⓇⓄⒿⒺⒸⓉ ⓪①",
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



# This api routes will display Airports data from 500 countries.
@app.get("/Airports/ Airports data")
async def airports2():
    
    """
    ### Airports data from 100 countries \n
    
    -    Id \n
    -    Airport Name \n
    -    City Name\n
    -    Country Name\n
    -    City 3 Letter Code\n
    -    City 4 Letter Code\n
    -    Latitude\n
    -    Longitude\n
    -    Elevation\n
    -    GMT \n
    -    Time Zone short\n
    -    Time zone\n
    -    Type\n
    -    Location in Hash\n
    
    """
    sql = "SELECT * FROM airports2 LIMIT 500 offset 3"
    
    with DatabaseCursor(".config.json") as cur:
        cur.execute(sql)
        return cur.fetchall()



# Top 100 Countries with the most Airports.
@app.get("/Airports/ Countries with the largest number of airports in a descending order")
async def airports2():
    """
    ### Top 100 Countries with the most Airports.
    
    """
   
    sql = "select country, COUNT(*) from airports2 GROUP BY COUNTRY ORDER BY COUNT(*) DESC limit 100"

    with DatabaseCursor(".config.json") as cur:
        cur.execute(sql)
        return cur.fetchall()

    
    
# This api routes is used to Display all the AIRPORTS between this longitude and latitude.
@app.get("/Airports/{lon}/{lat}")
async def airports2(lon: float, lat: float):
    """
    ### From the Longitude and Latitude it will display: 
    
    -   Airport Name
    -   City
    -   Country, 
    -   Three_code
    -   Time Zone
    -   Distance from that point.
    
    """
    sql = """select name, city, country, three_code, time_zone, 
            ST_Distance( 'SRID=4326;POINT(%s  %s)'::geometry, location) 
            AS dist FROM airports2 ORDER by dist ASC Limit 10;"""

    with DatabaseCursor(".config.json") as cur:
        cur.execute(sql, (lon, lat))
        return cur.fetchall()
    


# This api routes is used to display all the AIRPORTS from a specific country.
@app.get("/Airports/{country}")
async def airports2(country):
    """
    ### Display the data below from a specific country:\n
    
        -    Airports Name \n
        -    three_code\n
        -    Cities Name\n
        -    Time zone\n
        
        """
    sql = f"""SELECT name, three_code, city, Time_zone from airports2 
              WHERE country = '{country}'"""

    with DatabaseCursor(".config.json") as cur:
        cur.execute(sql)
        return cur.fetchall()


# This api routes is used to display all the AIRPORTS in a specific City.
@app.get("/Enter City")
async def airports2(city: str):
    """
    ### Display the data below from a specific City:\n
    
        -    Airports Name \n
        -    three_code
        -    Country
        -    Time zone\n
        
        """
    sql = f"""SELECT name, three_code, country, Time_zone from airports2 
              WHERE city = '{city}'"""

    with DatabaseCursor(".config.json") as cur:
        cur.execute(sql)
        return cur.fetchall()
    
# This api routes is used to display all the AIRPORTS in a specific three_code.
@app.get("/three_code")
async def airports2(three_code: str):
    """
    ### Display the data below from a specific City:\n
    
        -    Airports Name \n
        -    Cities Name\n 
        -    Country\n
        -    Time zone\n
        
        """
    sql = f"""SELECT name, city, country, Time_zone from airports2 
              WHERE three_code = '{three_code}'"""

    with DatabaseCursor(".config.json") as cur:
        cur.execute(sql)
        return cur.fetchall()
    

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
    


# This api routes will display the AIRPORTS from a specific country and city.
@app.get("/Enter Country and City")
async def airports2(country: str, city: str):
    """
    ### Display the data below from a specific country and city:\n
    
        -   Airport Name \n
        -   three_letter_code \n
        -   Country \n
        -   Time zone\n
        
        """
    sql = f"""SELECT name, country, three_code, time_zone from airports2 
              WHERE country = '{country}' AND city = '{city}'"""
              
    with DatabaseCursor(".config.json") as cur:
        cur.execute(sql)
        return cur.fetchall()
    
    
    
# This api routes will display Countries with more than 200 Airport.
@app.get("/Countries with more than 200 airports")
async def airports2():
    """
    ### Display Countries with more than 200 Airport.
     
    """
    sql = """SELECT country, COUNT(*) from airports2 GROUP BY COUNTRY HAVING COUNT(*) > 200 ORDER BY COUNT(*) DESC"""

    with DatabaseCursor(".config.json") as cur:
        cur.execute(sql)
        return cur.fetchall()



"""
            ░█▀▄▀█ ─█▀▀█ ▀█▀ ░█▄─░█ 
            ░█░█░█ ░█▄▄█ ░█─ ░█░█░█ 
            ░█──░█ ░█─░█ ▄█▄ ░█──▀█
"""

if __name__ == "__main__":
    uvicorn.run("api:app", port=8000, reload=True)