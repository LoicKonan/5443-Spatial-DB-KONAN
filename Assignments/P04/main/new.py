import time
import requests
import json
from re import S
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import psycopg2


# connection establishment
conn = psycopg2.connect(
    database="project3",
    user='postgres',
    password='kouassi',
    host='localhost',
    port='5432'
)
  
conn.autocommit = True
  
# Creating a cursor object
cursor = conn.cursor()


# write a function to download the data from the url http://missilecommand.live:8080/REGISTER in a csv file
def download_register_data():
    url = "http://missilecommand.live:8080/REGISTER"
    while True:
        try:
            register = requests.get(url)
            with open('register.csv', 'w') as f:
                json.dump(register.json(), f, indent=4)
                print(register.text)
            break
        except Exception:
            print("Connection error. Retrying in 5 seconds.")
            time.sleep(2)
            continue
        
        
# function to load the data from the csv file into the database using sql
def load_register_data():
    # query to import data from given csv
    sql = '''COPY register FROM 
            'C:\\Users\\loick\\OneDrive\\5443-Spatial DB-KONAN\\Assignments\\P04\main\\register.csv' DELIMITER ',' CSV HEADER'''
    
    # executing above query
    cursor.execute(sql)
    
    # Display the table
    cursor.execute('SELECT * FROM demo')
    print(cursor.fetchall())
    
    # Closing the connection
    conn.close()
                    
        
if __name__ == "__main__":
    download_register_data()
    load_register_data()
    

