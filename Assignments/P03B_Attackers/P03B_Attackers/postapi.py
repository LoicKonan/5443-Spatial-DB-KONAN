

from fastapi import FastAPI     # fast api
from pydantic import BaseModel  # to create class models

import uvicorn  # used as local mini server

class MissileSol(BaseModel):
    Lon1: float # starting X
    Lat1: float # starting Y
    Alt1: float # starting Z
    Time: int   # Time launched
    Type: int   # Missile Type
    Lon2: float # target X
    Lat2: float # target Y
    Alt2: float # target Z

app = FastAPI()

@app.post("/missileSolution/")
async def create_item(missSol: MissileSol):
   # print(missSol)
    return missSol

if __name__ == "__main__":
    uvicorn.run("postapi:app", host="127.0.0.1", port=8080, log_level="debug", reload=True)