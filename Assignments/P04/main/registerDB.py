import time
import requests
import json
from re import S
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import psycopg2

# write a function to download the data from the url http://missilecommand.live:8080/REGISTER
def download_register_data():
    url = "http://missilecommand.live:8080/REGISTER"
    while True:
        try:
            register = requests.get(url)
            with open('register.json', 'w') as f:
                json.dump(register.json(), f, indent=4)
                print(register.text)
            break
        except Exception:
            print("Connection error. Retrying in 5 seconds.")
            time.sleep(5)
            continue

if __name__ == "__main__":
    download_register_data()

