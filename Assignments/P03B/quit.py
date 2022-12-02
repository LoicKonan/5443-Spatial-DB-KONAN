import json
import requests

if __name__ == "__main__":

    # "Quit !!!
    # get the id from myregion.json
    with open("myregion.json") as f:
        data = json.load(f)
        id = data["id"]

    requests.get("http://missilecommand.live:8080/QUIT/" + str(id))
    print("Stop Sending them Damn Missiles to region " + str(id) + "!!!!!!")
