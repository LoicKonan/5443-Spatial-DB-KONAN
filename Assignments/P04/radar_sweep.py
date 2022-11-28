import time
import requests
import json
from re import S
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
import psycopg2
import json

url = "http://missilecommand.live:8080/RADAR_SWEEP"

if __name__=='__main__':

    while(True):
        time.sleep(5)
        missiles = requests.get(url)

        with open('missiles1.json', 'w') as f:
            json.dump(missiles.json(), f, indent=4)
            print(missiles.text)