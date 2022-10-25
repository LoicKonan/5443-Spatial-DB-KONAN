import time
import requests
import json

url = "http://localhost:8181/radar_sweep?gid=banditi"

if __name__=='__main__':
    while(True):
        time.sleep(1)
        r = requests.get(url)

        print(r.text)