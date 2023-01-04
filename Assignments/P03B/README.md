## Project 04  Missile Command (Part 2) 

### Loic Konan, Deangelo Brown, Byron Dowling

#### Description

- The goal of Missile Command (Part 2) is to detect all the enemy missiles and shoot them down.
- In order to accomplish our mission we had to:

  - Created tables call myregion and arsenal in our postgres Database, then insert the information that we receive from the server (<http://missilecommand.live:8080/START/)> in that table.
  
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

    - This will be be automatically perform by just running [register.py](register.py).
  
  - Perform Radar Sweep:
    - The Radar Sweep will create 2 missiles json to calculate bearing speed altitude and drop rate of the enemy missile.
  
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
      - This will be be automatically perform by just running [radar_sweep.py](radar_sweep.py).

  






### Example Response

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



### Instructions

- This program does not require any non standard libraries

### Example Command

- None for now.


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
