# generated by datamodel-codegen:
#   filename:  openapi.yaml
#   timestamp: 2020-10-20T23:52:57+00:00

from typing import Optional

from pydantic import BaseModel, Field, confloat, constr


class Webservice(BaseModel):
    status: Optional[str] = None
    version: Optional[str] = None


class Location(BaseModel):
    search_field: Optional[str] = Field(
        None, description='content of original search field\n'
    )
    latitude: Optional[confloat(ge=-90.0, le=90.0)] = Field(
        None, description='geocoded location\n'
    )
    longitude: Optional[confloat(ge=0.0, le=360.0)] = Field(
        None, description='geocoded location longitude\n'
    )
    rd_x: Optional[float] = Field(
        None,
        description='x coordinate in meters, geocoded location longitude transformed into EPSG:28992 \n',
    )
    rd_y: Optional[float] = Field(
        None,
        description='y coordinate in meters, geocoded location latitude transformed into EPSG:28992\n',
    )
    address: Optional[str] = Field(
        None, description='geocoded adress (street/house number)\n'
    )
    municipality: Optional[str] = Field(
        None, description='geocoded adress (municipality)\n'
    )
    zipcode: Optional[constr(regex='\d{4}[A-Z]{2}')] = Field(
        None, description='geocoded zipcode \n'
    )


class Data(BaseModel):
    flood_type: Optional[str] = None
    maximum_water_depth: Optional[float] = Field(
        None, description='maximum water depth in meters\n'
    )
    probability_of_flooding: Optional[confloat(ge=0.0, le=1.0)] = Field(
        None, description='expected frequency per year for flooding\n'
    )
    evacuation_percentage: Optional[float] = None
    safety_board_id: Optional[int] = None


class FloodInfo(BaseModel):
    webservice: Webservice
    location: Location
    data: Data
