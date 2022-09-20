## Project 02A - World Data with Postgres + Postgis

- []: # **Language:** _markdown_
- []: # **Path:** _README.md_
- []: # **Title:** _Project 02A_
- []: # **Author:** _[Loic_Konan](Loic_Konan)_
- []: # **Date:** _09/19/2022_
- []: # **Description:** _World Data with Postgres + Postgis_
- []: # **Tags:** **_[Postgres, Postgis]_**
  
  <br /><br />

## Loic Konan

### Description

- **Postgres + Postgis
- Downloaded and created tables to hold lots of data **(Airports, Rails, Roads, States, Timezones, Military Base data)**.
- Most of the data come from HERE(<https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html).com>
- Every tables has an **index on the spatial column** in your table, using **shp2pgsql**.
- This project loads shape files **(Rails, Roads, States, Timezones, Military Base data)** and a csv **(Airports)** into a postgres database using **pgadmin** and creates **Spatial indexes on those tables**.
- The **10** rows are displayed in a manner that is easy to read.

<br /><br />

<h2 align="center">The route above display the API documentation (Swagger). </h2>
<img src="fastapi.png">
<br /> <br /><br />

### Instructions

- Must have **Postgres** installed on your computer.
- Must have **Postgis** installed on your computer.

 <br />

### Files

|   #   | File / Folder                             | Description                                                    | Status                  |
| :---: | ----------------------------------------- | -------------------------------------------------------------- | ----------------------- |
|   1   | [README.md](README.md)                    | README file                                                    | :ballot_box_with_check: |
|   2   | [Datavisualization](./Datavisualiztion) | Display the output of each data as png                         | :ballot_box_with_check: |
|   3   | [InputData](./InputData)               | Airports, Rails, Roads, States, Timezones, Military Base data. | :ballot_box_with_check: |
|   4   | [Jsonfile](./Jsonfile)                  | All outputs in a json file.                                    | :ballot_box_with_check: |
|   5   | [SQLTables](./SQLTables)                | SQL files are in this folder                                   | :ballot_box_with_check: |
