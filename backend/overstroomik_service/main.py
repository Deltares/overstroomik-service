import logging
from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from overstroomik_service.auto_models import Data, FloodInfo, Location, Webservice
from overstroomik_service.config import settings
from overstroomik_service.errors import Errors
from overstroomik_service.geoserver import Geoserver
from overstroomik_service.pdok import PDOK

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return Webservice(
        version=settings.WS_VERSION, status=Errors.ERROR_GENERAL_IMEP.value
    )


@app.get("/by_rd", response_model=FloodInfo)
async def by_rd(x: float, y: float) -> FloodInfo:

    # Get location information from the geoserver
    status, data = await Geoserver.get_data(x, y)

    # Return location details
    return FloodInfo(
        webservice=Webservice(version=settings.WS_VERSION, status=status.value),
        location=Location(rd_x=x, rd_y=y),
        data=data,
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
        raise HTTPException(status_code=422, detail=Errors.ERROR_BY_LOCATION_422.value)

    data = Data()

    if status == Errors.ERROR_GENERAL_NOER:
        # Get location information from the geoserver
        status, data = await Geoserver.get_data(location.rd_x, location.rd_y)

    # Return location details
    return FloodInfo(
        webservice=Webservice(version=settings.WS_VERSION, status=status.value),
        location=location,
        data=data,
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
