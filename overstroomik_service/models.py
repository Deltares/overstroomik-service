from typing import Optional
from pydantic import BaseModel


class Location(BaseModel):
    searchfield: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]

    def resolve():
        pass


class Data(BaseModel):
    flood_type: str = "dijkring"

    @classmethod
    def from_location(cls, location: Location):
        # return cls(flood_type="")
        pass


class WebService(BaseModel):
    version: str = "v0.1"


class Response(BaseModel):
    webservice: WebService = WebService()
    data: Data = Data()
    location: Location
