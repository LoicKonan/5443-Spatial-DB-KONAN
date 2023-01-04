## Project 04  Missile Command (Part 2)

### Loic Konan, Deangelo Brown, Byron Dowling

#### Description

- The goal of Missile Command (Part 2) is to detect all the enemy missiles and shoot them down.
- In order to accomplish our mission we had to: <br><br>
  
  **1)** run the file [register.py](register.py), which will accomplish these below:
  - Created tables call **myregion** and **arsenal** in our postgres Database, then insert the information that we receive from the server (<http://missilecommand.live:8080/START/)> in the tables.
  
    - myregion is the region in the USA that I will be defending from the enemy incoming missiles.
    - arsenal is all the weapons/missiles that I will use to defend my region.

      ```json
          {
            "Atlas": 20,
            "Harpoon": 13,
            "Hellfire": 12,
            "Javelin": 11,
            "Minuteman": 9,
            "Patriot": 9,
            "Peacekeeper": 8,
            "SeaSparrow": 8,
            "Titan": 5,
            "Tomahawk": 4,
            "Trident": 1,
            "total": 10
          }
        ```

  <br><br>
  **2)**  run the file [radar_sweep.py](radar_sweep.py):
  - The Radar Sweep will create 2 missiles json to calculate bearing speed altitude and drop rate of the enemy missile.
  - <http://missilecommand.live:8080/RADAR_SWEEP>
    - [missile1.json](missile1.json) is use to see the geo-location of the incoming missiles.
    - [missile2.json](missile2.json) is use with the [missile1.json](missile1.json) to calculate the following:
      - Bearing
      - Speed
      - Altitude
      - Drop Rate
      - Missile geometry
      - Point to shoot the incoming missiles
      - Number of seconds to destroy the missiles
      - Time in which the intersection will occur
      - Missile Destination
      - Intersection points
      - Conversion of the time to return to the sever

  <br><br>
  **3)**  run the file [quit.py](quit.py):
  - <http://http://missilecommand.live:8080/QUIT>
  - The quit file will send the information to the server to Stop Sending them Damn Missiles to our region.

  <br><br>
  **4)**  run the file [solution.py](solution.py):
  - The solution file will first retrieve some information from our postgres Database and then send it to the server <http://missilecommand.live:8080/FIRE_SOLUTION/>

  - The information that we will send to the server are:

    - **team_id**           => get region id (rid) from myregion table
    - **target_missile_id** => Get the missile id from the table point_to_shoot
    - **missile_type**      => Get the missile type from the table speed database
    - **fired_time**        => Get the return time from the missile2 table.
    - **firedfrom_lat**     => Get the battery latitude from the table battery_lon_lat
    - **firedfrom_lon**     => Get the battery longitude from the table battery_lon_lat
    - **aim_lat**           => Get the target latitude from the table point_to_shoot
    - **aim_lon**           => Get the target latitude longitude from the table point_to_shoot
    - **expected_hit_time** => Get the return time from the return_time_hh_mm_ss table.
    - **target_alt**        => Get the target altitude from the table point_to_shoot_altitude

  <br><br>
  **5)**  run the file [GetStats.py](GetStats.py):
  - The GetStats file will retrieve the information from the server <http://missilecommand.live:8080/STATS/> and display it in the terminal.
  - This will display the missiles that we destroyed and the missiles that we missed in the terminal.
  
  <br><br>
  **6)**  run the file [reset.py](reset.py):
  - The reset file will reset the information that we got from the sever. <http://missilecommand.live:8080/RESET>

### Example Response


### Instructions

- To run the program, you will need to install the following:

  - [Python 3.7.3](https://www.python.org/downloads/release/python-373/)
  - [PostgreSQL 11.5](https://www.postgresql.org/download/)
  - [PostGIS 2.5.3](https://postgis.net/install/)
  - [psycopg2 2.8.3](https://pypi.org/project/psycopg2/)
  - [requests 2.22.0](https://pypi.org/project/requests/)
  - [geojson 2.5.0](https://pypi.org/project/geojson/)
  
- To run the program, you will need to create a database in PostgreSQL and then create the extension postgis in the database.

  - To create a database, type the following command in the terminal:

    ```bash
    createdb -U postgres -h localhost -p 5432 -W <database_name>
    ```

  - To create the extension postgis, type the following command in the terminal:

    ```bash
    psql -U postgres -h localhost -p 5432 -W <database_name>
    ```

    ```sql
    CREATE EXTENSION postgis;
    ```

### Example Command

- To run the program, type the following command in the terminal:

  ```bash
  python3 register.py
  python3 radar_sweep.py
  python3 quit.py
  python3 solution.py
  python3 GetStats.py
  python3 reset.py
  ```

### Files

|   #   | File                                 | Description                                       |
| :---: | ------------------------------------ | ------------------------------------------------- |
|   1   | [api.py](api.py)                     | The main file with comments and description       |
|   2   | [data.geojson](data.geojson)         | The geojson file with the region data             |
|   3   | [README.md](README.md)               | The file that you are currently reading           |
|   4   | [requirements.txt](requirements.txt) | The requirements file for the project             |
|   5   | [callPostApi.py](callPostApi.py)     | Call The Post file for the project                |
|   6   | [postApi.py](postApi.py)             | The postApi file for the project                  |
|   7   | [sql](./sql)                         | The sql folder with the sql files for the project |

### References

|   #   | File                                                                                                             | Description              |
| :---: | ---------------------------------------------------------------------------------------------------------------- | ------------------------ |
|   1   | [https://postgis.net/docs/ST_Buffer.html](https://postgis.net/docs/ST_Buffer.html)                               | ST_Buffer                |
|   2   | [https://postgis.net/docs/ST_Distance.html](https://postgis.net/docs/ST_Distance.html)                           | ST_Distance              |
|   3   | [https://postgis.net/docs/ST_Intersects.html](https://postgis.net/docs/ST_Intersects.html)                       | ST_Intersects            |
|   4   | [https://postgis.net/docs/ST_MakePoint.html](https://postgis.net/docs/ST_MakePoint.html)                         | ST_MakePoint             |
|   5   | [https://postgis.net/docs/ST_MakeLine.html](https://postgis.net/docs/ST_MakeLine.html)                           | ST_MakeLine              |
|   6   | [https://postgis.net/docs/ST_X.html](https://postgis.net/docs/ST_X.html)                                         | ST_X                     |
|   7   | [https://postgis.net/docs/ST_Y.html](https://postgis.net/docs/ST_Y.html)                                         | ST_Y                     |
|   8   | [https://postgis.net/docs/ST_Z.html](https://postgis.net/docs/ST_Z.html)                                         | ST_Z                     |
|   9   | [https://postgis.net/docs/ST_LineInterpolatePoints.html](https://postgis.net/docs/ST_LineInterpolatePoints.html) | ST_LineInterpolatePoints |
|  10   | [https://postgis.net/docs/ST_Envelope.html](https://postgis.net/docs/ST_Envelope.html)                           | ST_Envelope              |
|  11   | [https://postgis.net/docs/ST_AsGeoJSON.html](https://postgis.net/docs/ST_AsGeoJSON.html)                         | ST_AsGeoJSON             |
|  12   | [https://postgis.net/docs/ST_Area.html](https://postgis.net/docs/ST_Area.html)                                   | ST_Area                  |

### References Description

- **ST_Buffer** - Returns a geometry that represents all points whose distance from this Geometry is less than or equal to distance.
- **ST_Distance** - Returns the 2-dimensional cartesian minimum distance (based on spatial ref) between two geometries in projected units.
- **ST_Intersects** - Returns TRUE if the Geometries/Geography "spatially intersect in 2D" - (share any portion of space) and FALSE if they don't (they are Disjoint).
- **ST_MakePoint** - Returns a point geometry with the given x and y values.
- **ST_MakeLine** - Returns a LineString geometry formed from the given points.
- **ST_X** - Returns the X coordinate of the point.
- **ST_Y** - Returns the Y coordinate of the point.
- **ST_Z** - Returns the Z coordinate of the point.
- **ST_LineInterpolatePoints** - Returns a set of equidistant points along a LineString.
- **ST_Envelope** - Returns a geometry that represents the bounding box of this Geometry.
- **ST_Area** - Returns the area of the surface if it is a polygon or multi-polygon.
- **ST_AsGeoJSON** - Returns a GeoJSON representation of the geometry.
