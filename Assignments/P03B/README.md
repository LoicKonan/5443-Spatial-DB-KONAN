## Project 04  Missile Command (Part 2) 

### Loic Konan

#### Description

### `Region`

This function takes a `Point` and returns the `Region` that contains that point. If the point is not in any region, it returns `None`.
As stated in the previous assignment you will be defending a region against incoming missile attacks. The region you will defend will be assigned to you via an api call to `getRegion`. That call will return a geojson object with a list of features that will include:

* Boundary : 1 or more polygons defining your region
* Targets : Points defining the locations in which you are to defend
* Batteries : Points defining the location of your missile batteries

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
|   1   | [main.py](api.py)  | The main file with comments and description             |
|   2   | [README.md](README.md)  | The file that you are currently reading            |
|   3   | [sql](./sql) | The sql folder with the sql files for the project             |
|   4   | [myregion.geojson](myregion.geojson) | The region we defending                    |


### Instructions

- This program does not require any non standard libraries

### Example Command

- None for now.
