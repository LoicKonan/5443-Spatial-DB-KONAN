import requests

stats =  "http://missilecommand.live:8080/SHOW_STATS"
 
if __name__ == "__main__":

    # This will get the stats from the url.The response is a json object.
    response = requests.get(stats)
    
    # Print the response
    print(response.json())
    
