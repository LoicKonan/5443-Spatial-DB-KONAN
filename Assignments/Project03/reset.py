import requests

if __name__ == "__main__":

    # "RESET THE GAME!!!
    # Send a request to reset the game.
    requests.get("http://missilecommand.live:8080/RESET")
    print("Reset the Game ...")
