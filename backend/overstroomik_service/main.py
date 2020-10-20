from typing import Optional

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from overstroomik_service.config import settings
from overstroomik_service.auto_models import Data, FloodInfo, Webservice, Location

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/by_location", response_model=FloodInfo)
def by_location(
    search_field: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
) -> FloodInfo:
    # TODO
    # Derive location
    # Find location details in geoserver
    return FloodInfo(
        webservice=Webservice(),  # to be filled with eventual errors
        location=Location(
            search_field=search_field, latitude=latitude, longitude=longitude
        ),
        data=Data(),  # to be filled with data from geoserver
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
