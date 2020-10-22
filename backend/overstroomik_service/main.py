"""
This class uses the pdok-api to find address information

"""

from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from overstroomik_service.pdok import PDOK
from overstroomik_service.config import settings
from overstroomik_service.auto_models import Data, FloodInfo, Webservice, Location

WS_VERSION = 0.1
ERROR_GENERAL_NOER = "no-error"
ERROR_GENERAL_422 = "No valid input for search_field or latitude and longitude"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return Webservice(version=WS_VERSION, status=ERROR_GENERAL_NOER)


@app.get('/by_rd', response_model=FloodInfo)
async def by_rd(x: Optional[float] = None, y: Optional[float] = None) -> FloodInfo:

    # Get location information from the geoserver
    data = Data()

    return FloodInfo(
        webservice=Webservice(version=WS_VERSION, status=ERROR_GENERAL_NOER),
        location=Location(),
        data=data
    )


@app.get("/by_location", response_model=FloodInfo)
async def by_location(
    search_field: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
) -> FloodInfo:

    # Create pdok instance. 
    pdok = PDOK()

    # determine which pdok function by input 
    if search_field is not None and len(search_field.strip()) > 0:
        # Get address information from the PDOK services by search field
        status, location = await pdok.address_by_search_field(search_field)
    elif latitude and longitude:
        # Get address information from the PDOK services by latitude/ longitude
        status, location = await pdok.address_by_latlon(latitude, longitude)
    else:
        # No valid input for search_field or latitude and longitude
        raise HTTPException(status_code=422, detail=ERROR_GENERAL_422)

    data = Data()
    if status == ERROR_GENERAL_NOER:
        # Get location information from the geoserver
        data = Data()

    # Find location details in geoserver
    return FloodInfo(
        webservice=Webservice(version=WS_VERSION, status=status),
        location=location,
        data=data
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
