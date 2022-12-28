import time
import requests
from globals import MISSILE_GEN_INTERVAL
import asyncio

while True:
    try:
        x = requests.get("http://localhost:8080/bg")
    except Exception:
        time.sleep(.5)
