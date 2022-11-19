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

        
# function to load the data from the region0.json file into the database using sql
def loadData():
    # query to import data from given csv
    sql = '''COPY region0 FROM 
            'C:\\Users\\loick\\OneDrive\\5443-Spatial DB-KONAN\\Assignments\\P04\\main\\Region_0.json' DELIMITER ',' CSV HEADER'''
    
    # executing above query
    cursor.execute(sql)
    
    # Display the table
    cursor.execute('SELECT * FROM region0')
    print(cursor.fetchall())
    
    # Closing the connection
    conn.close()
    
  
                    
        
if __name__ == "__main__":
    loadData()
    

