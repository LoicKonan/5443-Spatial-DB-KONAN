import time
import requests
import json
from re import S
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
import psycopg2
import json

# write a program that will send a request with the teamID from the database to the API and then store the data in the database
url = "http://missilecommand.live:8080/START/registerID"

# connect to the database
