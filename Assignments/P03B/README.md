## Project 04  Missile Command (Part 2) 

### Deangelo Brown, Byron Dowling, Loic Konan

#### Description

### `getRegion`

This function takes a `Point` and returns the `Region` that contains that point. If the point is not in any region, it returns `None`.
As stated in the previous assignment you will be defending a region against incoming missile attacks. The region you will defend will be assigned to you via an api call to `getRegion`. That call will return a geojson object with a list of features that will include:

* Boundary : 1 or more polygons defining your region
* Targets : Points defining the locations in which you are to defend
* Batteries : Points defining the location of your missile batteries

[data.geojson](data.geojson)

### `getArsenal`

This route will send back a set of missiles that you have to defend your region. Don't worry about dividing up the missiles up amongst the batteries, we will assume any missile from your arsenal can be fired from any missile battery in your region. Below are a list of missiles and their classifications.


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
  "total": 100
}
```
   
### Files

|   #   | File                | Description                                            |
| :---: | ------------------  | -------------------------------------------            |
|   1   | [api.py](api.py)  | The main file with comments and description              |
|   2   | [data.geojson](data.geojson)  | The geojson file with the region data        |
|   3   | [README.md](README.md)  | The file that you are currently reading            |
|   4   | [requirements.txt](requirements.txt)  | The requirements file for the project|
|   5   | [callPostApi.py](callPostApi.py)  | Call The Post file for the project       |
|   6   | [postApi.py](postApi.py)  | The postApi file for the project                 |
|   7   |  [sql](./sql) | The sql folder with the sql files for the project            |



### References

|   #   | File                                                                                                                             | Description       |
| :---: | -------------------------------------------------------------------------------------------------------------------------------- | ----------------- |
|   1   | [https://postgis.net/docs/ST_Buffer.html](https://postgis.net/docs/ST_Buffer.html)                                               | ST_Buffer         |
|   2   | [https://postgis.net/docs/ST_Distance.html](https://postgis.net/docs/ST_Distance.html)                                           | ST_Distance       |
|   3   | [https://postgis.net/docs/ST_Intersects.html](https://postgis.net/docs/ST_Intersects.html)                                       | ST_Intersects     |
|   4   | [https://postgis.net/docs/ST_MakePoint.html](https://postgis.net/docs/ST_MakePoint.html)                                         | ST_MakePoint      |
|   5   | [https://postgis.net/docs/ST_MakeLine.html](https://postgis.net/docs/ST_MakeLine.html)                                           | ST_MakeLine       |
|   6   | [https://postgis.net/docs/ST_MakePolygon.html](https://postgis.net/docs/ST_MakePolygon.html)                                     | ST_MakePolygon    |
|   7   | [https://postgis.net/docs/ST_PointOnSurface.html](https://postgis.net/docs/ST_PointOnSurface.html)                               | ST_PointOnSurface |
|   8   | [https://postgis.net/docs/ST_X.html](https://postgis.net/docs/ST_X.html)                                                         | ST_X              |
|   9   | [https://postgis.net/docs/ST_Y.html](https://postgis.net/docs/ST_Y.html)                                                         | ST_Y              |
|  10   | [https://postgis.net/docs/ST_Z.html](https://postgis.net/docs/ST_Z.html)                                                         | ST_Z              |
|  11   | [http://postgis.net/docs/manual-1.5/ch04.html#PostGIS_Geography](http://postgis.net/docs/manual-1.5/ch04.html#PostGIS_Geography) | Geography Type    |
|  12   | [https://postgis.net/docs/ST_LineInterpolatePoints.html](https://postgis.net/docs/ST_LineInterpolatePoints.html)                 |ST_LineInterpolatePoints|
|  13   | [https://postgis.net/docs/ST_Envelope.html](https://postgis.net/docs/ST_Envelope.html)                                           | ST_Envelope       |
|  14   | [https://postgis.net/docs/ST_AsGeoJSON.html](https://postgis.net/docs/ST_AsGeoJSON.html)                                         | ST_AsGeoJSON      |
|  15   | [https://postgis.net/docs/Find_SRID.html](https://postgis.net/docs/Find_SRID.html)                                               | Find_SRID         |
|  16   | [https://postgis.net/docs/ST_Area.html](https://postgis.net/docs/ST_Area.html)                                                   | ST_Area           |

### References Description

- **ST_Buffer** - Returns a geometry that represents all points whose distance from this Geometry is less than or equal to distance.
- **ST_Distance** - Returns the 2-dimensional cartesian minimum distance (based on spatial ref) between two geometries in projected units.
- **ST_Intersects** - Returns TRUE if the Geometries/Geography "spatially intersect in 2D" - (share any portion of space) and FALSE if they don't (they are Disjoint).
- **ST_MakePoint** - Returns a point geometry with the given x and y values.
- **ST_MakeLine** - Returns a LineString geometry formed from the given points.
- **ST_MakePolygon** - Returns a polygon geometry formed from the given points.
- **ST_PointOnSurface** - Returns a point guaranteed to be on the surface of the geometry.
- **ST_X** - Returns the X coordinate of the point.
- **ST_Y** - Returns the Y coordinate of the point.
- **ST_Z** - Returns the Z coordinate of the point.
- **Geography Type** - A geography is a geometry that is stored in a projected coordinate system, but is interpreted as a geographic coordinate system.
- **ST_LineInterpolatePoints** - Returns a set of equidistant points along a LineString.
- **ST_Envelope** - Returns a geometry that represents the bounding box of this Geometry.
- **ST_AsGeoJSON** - Returns a GeoJSON representation of the geometry.
- **Find_SRID** - Returns the SRID of the geometry.
- **ST_Area** - Returns the area of the surface if it is a polygon or multi-polygon.
- **ST_LineInterpolatePoints** - Returns a set of equidistant points along a LineString.
- **ST_AsGeoJSON** - Returns a GeoJSON representation of the geometry.
- **Find_SRID** - Returns the SRID of the geometry.
- **ST_Area** - Returns the area of the surface if it is a polygon or multi-polygon.

### Instructions

- This program does not require any non standard libraries

### Example Command

- None for now.
