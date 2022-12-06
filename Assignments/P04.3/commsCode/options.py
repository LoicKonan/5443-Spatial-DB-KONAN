import http.client
import requests
import json



HASH_KEY = "61ec12b68d0ded5f6a84b7d1f6d4d8e70695c2ba5dd7176fc3e4c3d53db9ecf2"
FLEETNAME = "poseidon"

GAME_ID = 0

def start_game():
    url = f"https://battleshipgame.fun:8080/generate_fleet/?fleetName={FLEETNAME}&hash={HASH_KEY}"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    if response.ok == True:
        print("Game has been started!!")
    else:
        print("Error game was unable to start :(")

def generate_fleet():
    url = f"https://battleshipgame.fun:8080/generate_fleet/?fleetName={FLEETNAME}&hash={HASH_KEY}"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()

    if response.ok == True:
        with open("ships.json", "w") as file:
            json.dump(data, file, indent=4)
        return data
    else:
        return "ERROR!!!!"    
    
def create_game():
    url = f"https://battleshipgame.fun:8080/create_game/?hash={HASH_KEY}&game_name={FLEETNAME}"
    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    print({"Game information": response.json()})


def current_game():
    hold = []
    url = f"https://battleshipgame.fun:8080/current_games/?hash={HASH_KEY}"
    payload={}
    headers = {}
    global GAME_ID
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    hold.append(data)

    with open("current.json", "w") as file:
        json.dump(data, file, indent=4)

    with open("current.json", "r") as f:
        game = json.loads(f.read()) 

        for ga in game["data"]:
            if ga["game_name"] == "poseidon":
                GAME_ID = ga["game_id"]
    
    print("Your game id =" + str(GAME_ID))


def get_a_location():
    url = f"https://battleshipgame.fun:8080/get_battle_location/?hash={HASH_KEY}&game_id={GAME_ID}"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    #print(data)
    print( {"bbox": data["bbox"], "CardinalLocation": data["section"]})

def turn_ship():
    url = "https://battleshipgame.fun:1234/turn_ship/"

    with open("final_product.json", "r") as f:
        data = json.loads(f.read())
        ship_info = []
        bearings_info = []
        for i in data["ship_status"]:
            fleet = data["fleet_id"]
            ship_info.append(i["ship_id"])
            bearings_info.append(i["bearing"])

    payload = json.dumps({
        "fleet_id": fleet,
        "ship_id": ship_info,
        "bearing": bearings_info
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == requests.codes.ok:
        return 'Success'
    else:
        return "error"


