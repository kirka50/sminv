from typing import Optional

import json
import uvicorn
from BaseFunctionsFromDB import *
from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


from pydantic import BaseModel

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class item(BaseModel):
    inv: int
    name: str
    met: str
    curkab: int
    parkab: int
    status: int

class do(BaseModel):
    value1: int
    value2: int
@app.get("/getDataByRFID/{Rf_ID}")
def findDataByRfID(Rf_ID):
    Rf_ID = placeRazdelitel(Rf_ID)
    data = findByRdID(Rf_ID)
    return data
@app.get("/pick/{Rf_ID}/{CurrentCab}")
def sendToNeironRfidAndCurcab(Rf_ID,CurrentCab):
    visual(placeRazdelitel(Rf_ID),int(CurrentCab))
    return {"Status": "Ok"}
@app.get("/FindBadMebel")
def findBadMeb():
    data = findBadMebel()
    return data
@app.get("/FindBadObur")
def findBadOb():
    data = findBadObur()
    return {data}

@app.get("/FindBadElec")
def findBadEl():
    data = findBadElec()
    return data
@app.get("/FindByExcelNumber")
def findByExcelNumber():
    data = findByOldExcelNumber()
    return data

@app.get("/")
def g(*, Hello: str = Header('abc')):
    return {"Hello": Hello}
@app.get("/get")
def hello(number):
    return {"number": number}
@app.post("/see")
def create_item(item: item):

    return item

@app.post("/odd")
def see(re: do):
    return do

def placeRazdelitel(Stirng):
    Stirng = Stirng[:2] + ":" + Stirng[2:4] + ":" + Stirng[4:6] + ":" + Stirng[6:8]
    print (Stirng)
    return (str(Stirng))

if __name__ == "__main__":
    uvicorn.run("FastApiServer:app", host="0.0.0.0", port=8000, log_level="info")
