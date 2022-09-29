## Project 03  Missile Command (Part 1) 

### Loic Konan

#### Description

- Missile Command was an 80's arcade game in which the player had to defend earth using anti-missile batteries that shot defensive "clouds" into the air (see animation).
- We will create our own "no graphics" implementation of the game incorporating our spatial db concepts.
- This first part of the game is to determine how many military bases, and to generate a series of missile paths which intersect with a military base and get shot down.
- The second part we will attempt to do something in real time with missiles coming at different speeds and altitudes, and each military base will have limited reaction time, giving them a chance to get hit. This first part is only generating random paths and simple line v polygon intersection recognition.

#### Data

1. [US_Military_Base](US_Military_Bases) - This is a list of military bases in the US.
2. Random Missile Paths

### Files

|   #   | File               | Description                                 |
| :---: | ------------------ | ------------------------------------------- |
|   1   | [main.py](main.py) | The main file with comments and description |

### References


|   #   | File                                                                                                                             | Description       |
| :---: | -------------------------------------------------------------------------------------------------------------------------------- | ----------------- |
|   1   | [https://postgis.net/docs/ST_Buffer.html](https://postgis.net/docs/ST_Buffer.html)                                               | ST_Buffer         |
|   2   | [https://postgis.net/docs/ST_Distance.html](https://postgis.net/docs/ST_Distance.html)                                           | ST_Distance       |
|   3   | [https://postgis.net/docs/ST_GeomFromText.html](https://postgis.net/docs/ST_GeomFromText.html)                                   | ST_GeomFromText   |
|   4   | [https://postgis.net/docs/ST_Intersects.html](https://postgis.net/docs/ST_Intersects.html)                                       | ST_Intersects     |
|   5   | [https://postgis.net/docs/ST_MakePoint.html](https://postgis.net/docs/ST_MakePoint.html)                                         | ST_MakePoint      |
|   6   | [https://postgis.net/docs/ST_MakeLine.html](https://postgis.net/docs/ST_MakeLine.html)                                           | ST_MakeLine       |
|   7   | [https://postgis.net/docs/ST_MakePolygon.html](https://postgis.net/docs/ST_MakePolygon.html)                                     | ST_MakePolygon    |
|   8   | [https://postgis.net/docs/ST_Multi.html](https://postgis.net/docs/ST_Multi.html)                                                 | ST_Multi          |
|   9   | [https://postgis.net/docs/ST_PointOnSurface.html](https://postgis.net/docs/ST_PointOnSurface.html)                               | ST_PointOnSurface |
|  10   | [https://postgis.net/docs/ST_Transform.html](https://postgis.net/docs/ST_Transform.html)                                         | ST_Transform      |
|  11   | [https://postgis.net/docs/ST_X.html](https://postgis.net/docs/ST_X.html)                                                         | ST_X              |
|  12   | [https://postgis.net/docs/ST_Y.html](https://postgis.net/docs/ST_Y.html)                                                         | ST_Y              |
|  13   | [https://postgis.net/docs/ST_Z.html](https://postgis.net/docs/ST_Z.html)                                                         | ST_Z              |
|  14   | [https://postgis.net/docs/ST_ZMFlag.html](https://postgis.net/docs/ST_ZMFlag.html)                                               | ST_ZMFlag         |
|  15   | [https://postgis.net/docs/ST_ZMax.html](https://postgis.net/docs/ST_ZMax.html)                                                   | ST_ZMax           |
|  16   | [https://postgis.net/docs/ST_ZMin.html](https://postgis.net/docs/ST_ZMin.html)                                                   | ST_ZMin           |
|  17   | [https://postgis.net/docs/ST_ZRange.html](https://postgis.net/docs/ST_ZRange.html)                                               | ST_ZRange         |
|  18   | [https://postgis.net/docs/ST_Zmflag.html](https://postgis.net/docs/ST_Zmflag.html)                                               | ST_Zmflag         |
|  19   | [http://postgis.net/docs/manual-1.5/ch04.html#PostGIS_Geography](http://postgis.net/docs/manual-1.5/ch04.html#PostGIS_Geography) | Geography Type    |
|  20   | [https://postgis.net/docs/ST_LineInterpolatePoints.html](https://postgis.net/docs/ST_LineInterpolatePoints.html)                 |ST_LineInterpolatePoints|
|  21   | [https://postgis.net/docs/ST_Envelope.html](https://postgis.net/docs/ST_Envelope.html)                                           | ST_Envelope |
|  22   | [https://postgis.net/docs/ST_Dump.html](https://postgis.net/docs/ST_Dump.html)                                                   | ST_Dump |
|  23   | [https://postgis.net/docs/ST_DumpPoints.html](https://postgis.net/docs/ST_DumpPoints.html)                                       | ST_DumpPoints |
|  24   | [https://postgis.net/docs/ST_DumpRings.html](https://postgis.net/docs/ST_DumpRings.html)                                         | ST_DumpRings |
|  25   | [https://postgis.net/docs/ST_DumpLines.html](https://postgis.net/docs/ST_DumpLines.html)                                         | ST_DumpLines |
|  26   | [https://postgis.net/docs/ST_DumpPolygons.html](https://postgis.net/docs/ST_DumpPolygons.html)                                   | ST_DumpPolygons |
|  27   | [https://postgis.net/docs/ST_AsGeoJSON.html](https://postgis.net/docs/ST_AsGeoJSON.html)                                         | ST_AsGeoJSON |
|  32   | [https://postgis.net/docs/Find_SRID.html](https://postgis.net/docs/Find_SRID.html)                                               | Find_SRID |
|  33   | [https://postgis.net/docs/ST_Area.html](https://postgis.net/docs/ST_Area.html)                                                   | ST_Area |

### Instructions

- This program does not require any non standard libraries

### Example Command

- None for now.
