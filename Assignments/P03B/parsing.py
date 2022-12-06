import json
import copy
import itertools
import re


MissileResponses = []

MissileResponse = {
    "team_id": 0,
    "target_missile_id": 0,
    "missile_type": "string",
    "fired_time": "string",
    "firedfrom_lat": 0,
    "firedfrom_lon": 0,
    "aim_lat": 0,
    "aim_lon": 0,
    "expected_hit_time": "string",
    "target_alt": 0
}

# Open file 
# Fin = open('solution.json')

# # Read json
# data = json.load(Fin)


# with open("solution.json") as Fin:
#     data = json.load(Fin)
#     # print(data)
    
    
    

#     MissileResponses.extend(value[0] for key, value in data.items())
#     merged = list(itertools.chain(*MissileResponses))
#     #print(merged)

# for i in MissileResponse:
#     i = MissileResponses


# print(MissileResponses)
# print("\n")
# print(MissileResponse)


# go to solution.json and get the first of each key and the value.
# then go to the value and get the first element and value.
with open("solution.json") as data:
    data = json.load(data)
    for key, value in data.items():
        print(key,value[0][0])
        
        # send it to a json.
        with open("solution1.json", "a") as f:
            json.dump((key,value[0][0]), f)
            f.write("\n")            
        
            
            
            
            
            
        
        
    
        
        
        