# generated by datamodel-codegen:
#   filename:  openapi.yaml
#   timestamp: 2020-10-30T07:47:22+00:00

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, confloat, constr, validator


class Webservice(BaseModel):
    status: Optional[str] = Field(None, example='no-error')
    version: Optional[str] = Field(None, example='overstroomik webservice 1.0.0')


class Location(BaseModel):
    search_field: Optional[str] = Field(
        None, description='content of original search field\n', example='8232JN'
    )
    latitude: Optional[confloat(ge=-90.0, le=90.0)] = Field(
        None, description='geocoded location\n', example=52.5066973961792
    )
    longitude: Optional[confloat(ge=0.0, le=360.0)] = Field(
        None, description='geocoded location longitude\n', example=5.46887674785145
    )
    rd_x: Optional[float] = Field(
        None,
        description='x coordinate in meters, geocoded location longitude transformed into EPSG:28992 \n',
        example=160544.902,
    )
    rd_y: Optional[float] = Field(
        None,
        description='y coordinate in meters, geocoded location latitude transformed into EPSG:28992\n',
        example=502115.495,
    )
    address: Optional[str] = Field(
        None, description='geocoded adress (street/house number)\n', example='Botter 11'
    )
    municipality: Optional[str] = Field(
        None, description='geocoded adress (municipality)\n', example='Lelystad'
    )
    zipcode: Optional[constr(regex='\d{4}[A-Z]{2}')] = Field(
        None, description='geocoded zipcode \n', example='8232JN'
    )


class FloodType(Enum):
    binnen_dijkring__mogelijk_overstroombaar = (
        'binnen dijkring, mogelijk overstroombaar'
    )
    buiten_dijkring__geen_hogegrond__buitendijks_of_buiten_water_ = (
        'buiten dijkring, geen hogegrond (buitendijks of buiten water)'
    )
    buiten_dijkring__hogegrond = 'buiten dijkring, hogegrond'


class ProbabilityOfFlooding(Enum):
    geen_significante_overstromingskans = 'geen significante overstromingskans'
    grote_kans____1_30_per_jaar = 'grote kans: > 1/30 per jaar'
    middelgrote_kans__1_30_tot_1_300_per_jaar = (
        'middelgrote kans: 1/30 tot 1/300 per jaar'
    )
    kleine_kans__1_300_tot_1_3_000_per_jaar = 'kleine kans: 1/300 tot 1/3.000 per jaar'
    zeer_kleine_kans__1_3_000_tot_1_30_000_per_jaar = (
        'zeer kleine kans: 1/3.000 tot 1/30.000 per jaar'
    )
    extreem_kleine_kans____1_30_000_per_jaar = (
        'extreem kleine kans: < 1/30.000 per jaar'
    )


class Data(BaseModel):
    flood_type: Optional[FloodType] = Field(
        None,
        description='type of flooding area\n',
        example='binnen dijkring, mogelijk overstroombaar',
    )
    maximum_water_depth: Optional[confloat(ge=0.0)] = Field(
        None, description='maximum water depth in meters\n', example=3.2242
    )
    probability_of_flooding: Optional[ProbabilityOfFlooding] = Field(
        None,        
        description='expected frequency per year for flooding\n',
        example='kleine kans: 1/300 tot 1/3.000 per jaar',
    )
    evacuation_percentage: Optional[confloat(ge=0.0, le=100.0)] = Field(
        None,
        description='expected evacuation percentage\nif percentage ≤ 20 then ‘vrijwel niemand kan het gebied verlaten’\nif percentage ≤ 40 then ‘een klein deel kan het gebied verlaten’\nif percentage ≤ 60 then ‘ongeveer de helft kan het gebied verlaten’\nif percentage ≤ 80 then ‘een groot deel kan het gebied verlaten’\nif percentage > 80 then ‘vrijwel iedereen kan het gebied verlaten’\n',
        example=35,
    )
    safety_board_id: Optional[int] = Field(
        None, description='unique id of safety board\n', example=12
    )

    @validator('maximum_water_depth', pre=True)
    def validator_maximum_water_depth(cls, value):

        # water depth lower then one cm is to low or no valid data from the layer
        if value < 0.01:
            value = 0.0

        # water depth more then 50 m is no water is to high or no valid data from the layer
        elif value > 50.0:
            value = 0.0

        return value

    @validator('probability_of_flooding', pre=True)
    def validator_probability_of_flooding(cls, value):
        
        # No action as the enum parse is passed
        if isinstance(value, ProbabilityOfFlooding):
            return value
        else:
            if value == None:
                return None
            elif value.lower() == "geen significante overstromingskans":
                return ProbabilityOfFlooding.geen_significante_overstromingskans
            elif value.lower() == "grote kans: > 1/30 per jaar":
                return ProbabilityOfFlooding.grote_kans____1_30_per_jaar
            elif value.lower() == "middelgrote kans: 1/30 tot 1/300 per jaar":
                return ProbabilityOfFlooding.middelgrote_kans__1_30_tot_1_300_per_jaar
            elif value.lower() == "kleine kans: 1/300 tot 1/3.000 per jaar":
                return ProbabilityOfFlooding.kleine_kans__1_300_tot_1_3_000_per_jaar
            elif value.lower() == "zeer kleine kans: 1/3.000 tot 1/30.000 per jaar":
                return ProbabilityOfFlooding.zeer_kleine_kans__1_3_000_tot_1_30_000_per_jaar
            elif value.lower() == "extreem kleine kans: < 1/30.000 per jaar":
                return ProbabilityOfFlooding.extreem_kleine_kans____1_30_000_per_jaar
            else:
                return None

    @validator('flood_type', pre=True)
    def validator_flood_type(cls, value):

        # No action as the enum parse is passed
        if isinstance(value, FloodType):
            return value
        else:
            if value == None:
                return None
            elif value.lower() == "binnen dijkring, mogelijk overstroombaar":
                return FloodType.binnen_dijkring__mogelijk_overstroombaar
            elif value.lower() == "buiten dijkring, geen hogegrond (buitendijks of buiten water)":
                return FloodType.buiten_dijkring__geen_hogegrond__buitendijks_of_buiten_water_
            elif value.lower() == "buiten dijkring, hogegrond":
                return FloodType.buiten_dijkring__hogegrond
            else:
                return None


class FloodInfo(BaseModel):
    webservice: Webservice
    location: Location
    data: Data
