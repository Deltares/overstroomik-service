"""
This class uses the pdok-api to find address information

"""

from typing import Optional
from pydantic import BaseModel
from overstroomik_service.auto_models import Data, FloodInfo, Webservice, Location
from overstroomik_service.config import settings
import httpx


class PDOK():

    # api url (exampl:https://geodata.nationaalgeoregister.nl/locatieserver/v3/free)
    api = settings.PDOK_API
    fields = "centroide_rd,centroide_ll,straatnaam,woonplaatsnaam,postcode"

    async def get_address(self, 
                          searchfield: Optional[str], 
                          latitude: Optional[float], 
                          longitude: Optional[float]):
        """
        Search address information from the PDOK services.
        """

        adress_item = {}

        # start with no errors
        status = settings.ERROR_GENERAL_NOER

        # search by text or by lat/lon
        if searchfield is not None and len(searchfield.strip()) > 0:
            status, adress_item = await self.address_by_searchfield(searchfield)
        elif latitude and longitude:
            status, adress_item = await self.address_by_latlon(latitude, longitude)
        else:
            status = settings.ERROR_GENERAL_ERRO

        # return status and location
        return status, Location(
            search_field=searchfield,
            latitude=adress_item.get("latitude", latitude),
            longitude=adress_item.get("longitude", longitude),
            rd_x=adress_item.get("rd_x", None),
            rd_y=adress_item.get("rd_y", None),
            address=adress_item.get("address", ""),
            municipality=adress_item.get("municipality", ""),
            zipcode=adress_item.get("zipcode", None)
        )

    async def address_by_searchfield(self, 
                                     searchfield: str):
        """
        Search address information with specified search string.
        """
        # initieel no error
        status = settings.ERROR_GENERAL_NOER
        
        # start with empty object
        adress_item = {}

        # build api_url
        url = f"{self.api}?q={searchfield}&rows=1&fl={self.fields}"

        # connect async to the pdok-api
        async with httpx.AsyncClient() as client:
            result = await client.get(url, timeout=10.0)

            if result.status_code == httpx.codes.OK:
                status, adress_item = self.list_to_location(result.json())
            else:
                status = settings.ERROR_PDOK_NO_RESP

        # return status and address information
        return status, adress_item

    async def address_by_latlon(self, latitude: float, longitude: float):
        """
        Search address information with specified latitude and longitude.
        """
        # initieel no error
        status = settings.ERROR_GENERAL_NOER
        
        # start with empty object
        adress_item = {}

        # build api_url
        url = f"{self.api}?q=type:adres&lat={latitude}&lon={longitude}&rows=1&fl={self.fields}"

        # connect async to the pdok-api
        async with httpx.AsyncClient() as client:
            result = await client.get(url, timeout=10.0)

            if result.status_code == httpx.codes.OK:
                status, adress_item = self.list_to_location(result.json())
            else:
                status = settings.ERROR_PDOK_NO_RESP

        # return status and address information
        return status, adress_item

    def list_to_location(self, out: dict):
        """
        Get the best result from de list (now 1 row with highest score)
        """
        # initieel no error
        status = settings.ERROR_GENERAL_NOER
        
        adress_item = {}
        response = out.get("response")
        
        if response.get("numFound", 0) > 0:
            docs = response.get("docs")
            if len(docs) > 0:
                # Use the first result, this one has the highest score.
                adress_item = self.to_location(docs[0])
            else:
                status = settings.ERROR_PDOK_NO_RESU
        else:
            status = settings.ERROR_PDOK_NO_RESU

        return status, adress_item

    def to_location(self, doc_item: dict):
        """
        Translate pdok-item to location
        """

        rd = doc_item.get("centroide_rd", "0 0").replace("POINT(",
                                                         "").replace(")", "").split(" ")
        ll = doc_item.get("centroide_ll", "0 0").replace("POINT(",
                                                         "").replace(")", "").split(" ")

        return {
            "latitude": ll[0],
            "longitude": ll[1],
            "rd_x": rd[0],
            "rd_y": rd[1],
            "address": doc_item.get("straatnaam", None),
            "municipality": doc_item.get("woonplaatsnaam", None),
            "zipcode": doc_item.get("postcode", None),
        }
