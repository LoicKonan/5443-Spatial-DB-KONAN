import time
import requests
import json
from re import S
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
import psycopg2
import json

url = "http://missilecommand.live:8080/REGISTER"

if __name__=='__main__':
    register = requests.get(url)

    with open('register.json', 'w') as f:
        json.dump(register.json(), f, indent=4)
        print(register.text)