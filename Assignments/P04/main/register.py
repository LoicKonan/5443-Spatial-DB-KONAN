import time
import requests
import json
from re import S
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
import psycopg2

url = "http://missilecommand.live:8080/REGISTER"

if __name__ == "__main__":
    while True:
        try:
            register = requests.get(url)
            with open('region.json', 'w') as f:
                json.dump(register.json(), f, indent=4)
                print(register.text)
            break
        except Exception:
            print("Connection error. Retrying in 5 seconds.")
            time.sleep(5)
            continue
    print("Registered with game server.")
    print("Starting server.")