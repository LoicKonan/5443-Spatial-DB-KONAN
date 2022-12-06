## Project 4
#### 11/16/2022
## Missile Command
# 

#### Description: 
This assignment uses FastAPI and Digital Ocean to implement a server to hold routes for a missile command game.
The intention of this game is to have one side serve as the attackers and the other side to defend against missiles
being targeted at specific points in their given region using PostgreSQL and PostGIS for database and spatial querying.
This code is for the implementation of the attacker side of the game. The routes available for Missile Command for 
defenders to receive are:
- register
  - obtain a region to defend and how much arsenal they have to defend their region with
- start
  - notify the attacker side that you are ready to begin having missile target your region
- radar_sweep
  - see all the missles flying over the continental United States at a given time and where each one currently is
- fire_solution
  - receive information from defender side wanting to hit a missile out of the air and verify if there was a hit
- stop
  - surrender and have the attackers stop sending missiles to your region
- reset
  - reset the game and allow for past regions to be given to new teams. also resets the database for a brand new game.
- see_stats
  - see how many missiles a given region received and how many they hit
  
The generation of missiles is done using a background process and a missile is generated every 5 seconds for all regions that have
started the game. Each missile is updated every second to mimic real time. There are various types of missiles of which some are slow but contain a large explosion blast radius and others are fast but not as explosive. Depending on the missile and where it was generated from, 
a missle could reach a region anywhere between 30 seconds to a little under 3 minutes in real time. This is to allow for real time simulation to occur in order to not be too idle waiting for a missile to get closer to a region. All missiles are generated on the outer border of a bounding box covering the continental United States. When a missile from the defending team is sent to deflect an active missile, it is then verified by the attacking side. The blast radius of both missiles is taken into account at the moment of impact. If the
blasts overlap, then it is considered that the missiles hit each other and the hit was successful. Both the longitude and latitude 
coordinates must be within the blast radius as well as the missiles altitude. At the end of the game, defenders can view how many
missiles were sent to their specific region and how many missiles they managed to hit flying overhead. Once the game has finished, 
it can be reset to be played again if desired.

### Main Files:
|   #   | File Link | Description |
| :---: | ----------- | ---------------------- |
|  01  | [api.py](https://github.com/apwarren/5443-Spatial-DB-Warren/tree/master/Assignments/P04/api.py) | main python file. Contains all code for generating, updating, and verifying missiles as well as route calls |
|  02  | [background.py](https://github.com/apwarren/5443-Spatial-DB-Warren/tree/master/Assignments/P04/background.py) | python file containing the background process for missile generation and updating while waiting for api calls |
