from comms import CommsListener

# example game user
creds = {
    "exchange": "battleship",
    "port": "5672",
    "host": "battleshipgame.fun",
    "user": "us_navy",
    "password": "rockpaperscissorsrabbitdonkey",
    "hash": "61ec12b68d0ded5f6a84b7d1f6d4d8e70695c2ba5dd7176fc3e4c3d53db9ecf2",
}

print("Comms Listener starting. To exit press CTRL+C ...")
# create instance of the listener class and sending in the creds
# object as kwargs
commsListener = CommsListener(**creds)

# tell rabbitMQ which 'topics' you want to listen to. In this case anything
# with the team name in it (user) and the broadcast keyword.
commsListener.bindKeysToQueue([f"#.{creds['user']}.#", "#.broadcast.#"])

# now really start listening
commsListener.startConsuming()