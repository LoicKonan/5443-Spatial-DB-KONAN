## Program 1 - Project setup

### Loic Konan

#### Description

- Database
Have local install of Postgres dB with PostGis installed and enabled.
Visualization tools (e.g. Pgadmin4) recommended to allow myself or others to help debug problems.
Create a DB called Project1 and use the public schema for this project.
Find a data file from https://cs.msutexas.edu/~griffin/data and load it into your DB. Obviously create an appropriate table with a geometry data type added to allow for some spatial query's to be run.
Api
Have a local api that has the following routes:
findAll
findOne
findClosest
findAll
Returns all the tuples from your table
findOne
Returns a single tuple based on a column name (attribute) and value (e.g id=1299 , or name=texas).
findClosest
Returns a single tuple which contains the closest geometry to the one passed in (e.g. lon=-123.63454&lat=34.74645)

### Files

|   #   | File                         | Description                                |
| :---: | ---------------------------- | ------------------------------------------ |
|   1   | [main.cpp](main.cpp)         | The main cpp with comments and description |
                                |

### Instructions

- This 

### Example Command

- None for now.