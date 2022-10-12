import requests
import json

url = "http://localhost:8080/missileSolution"

payload = json.dumps({
  "Lon1": -98.4,
  "Lat1": 34.9,
  "Alt1": 1,
  "Time": 2625252,
  "Type": 8,
  "Lon2": -123.8,
  "Lat2": 32.777,
  "Alt2": 11111
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)