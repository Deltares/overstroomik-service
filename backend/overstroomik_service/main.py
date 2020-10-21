"""
This class uses the pdok-api to find address information

"""

from typing import Optional

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from overstroomik_service.pdok import PDOK
from overstroomik_service.config import settings
from overstroomik_service.auto_models import Data, FloodInfo, Webservice, Location
from overstroomik_service.rijksdriehoek import Rijksdriehoek

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return Webservice(version=settings.WS_VERSION, status=settings.ERROR_GENERAL_NOER)


@app.get('/by_rd', response_model=FloodInfo)
async def by_rd(x: Optional[float] = None, y: Optional[float] = None) -> FloodInfo:

    # initieel no error
    status = settings.ERROR_GENERAL_NOER

    # Convert rd to lat/lon
    rijksdriehoek = Rijksdriehoek()
    latlon = rijksdriehoek.rd_to_wgs(x, y)
    print (len(latlon))
    # Get address information from the PDOK services
    pdok = PDOK()
    status, location = await pdok.get_address(searchfield=None, latitude=latlon[0], longitude=latlon[1])

    data = Data()
    if status == settings.ERROR_GENERAL_NOER:
        # Get location information from the geoserver
        data = Data()

    return FloodInfo(
        webservice=Webservice(version=settings.WS_VERSION, status=status),
        location=location,
        data=data
    )


@app.get("/by_location", response_model=FloodInfo)
async def by_location(
    search_field: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
) -> FloodInfo:

    # initieel no error
    status = settings.ERROR_GENERAL_NOER

    # Get address information from the PDOK services
    pdok = PDOK()
    status, location = await pdok.get_address(searchfield=search_field, latitude=latitude, longitude=longitude)

    data = Data()
    if status == settings.ERROR_GENERAL_NOER:
        # Get location information from the geoserver
        data = Data()

    # Find location details in geoserver
    return FloodInfo(
        # to be filled with eventual errors
        webservice=Webservice(version=settings.WS_VERSION, status=status),
        location=location,
        data=data
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
