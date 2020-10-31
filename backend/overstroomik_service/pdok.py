"""
This class uses the pdok-api to find address information

"""
import logging

import httpx

from overstroomik_service.auto_models import Location
from overstroomik_service.config import settings
from overstroomik_service.errors import Errors


class PDOK:

    # pdok api url
    api = "https://geodata.nationaalgeoregister.nl/locatieserver/v3/free"

    # fields we need
    fields = "centroide_rd,centroide_ll,straatnaam,woonplaatsnaam,postcode"

    async def address_by_search_field(self, search_field: str):
        """
        Search address information with specified search string.
        :param search_field: content of original search field
        """
        # input parameters for pdok-api
        params = {"q": search_field, "rows": 1, "fl": self.fields}

        # fetch date and return address
        status, address_item = await self.fetch_data(url=self.api, params=params)

        address_item["search_field"] = search_field

        return status, Location(**address_item)

    async def address_by_latlon(self, latitude: float, longitude: float):
        """
        Search address information with specified latitude and longitude.
        :param latitude: coordinate in degrees in EPSG:4326
        :param longitude: coordinate in degrees in EPSG:4326
        """

        # input parameters for pdok-api
        params = {
            "q": "type:adres",
            "lat": latitude,
            "lon": longitude,
            "rows": 1,
            "fl": self.fields,
        }

        # fetch date and return address
        status, address_item = await self.fetch_data(url=self.api, params=params)

        return status, Location(**address_item)

    async def fetch_data(self, url: str, params: dict):
        """
        Get the data from PDOK
        :param url: api url to fetch
        """
        address_item = {}

        # connect async to the pdok-api
        async with httpx.AsyncClient() as client:

            # fetch the feature info
            try:
                result = await client.get(
                    url=url, params=params, timeout=settings.FETCH_TIMEOUT
                )
                if result.status_code == httpx.codes.OK:
                    status, address_item = self.list_to_location(result.json())
                else:
                    status = Errors.ERROR_PDOK_NO_RESP

            except httpx.RequestError as exc:
                logging.exception(
                    f"Failed to connect to PDOK using {exc.request.url!r}"
                )
                status = Errors.ERROR_PDOK_NO_RESP

        # return status and address information
        return status, address_item

    def list_to_location(self, out: dict):
        """
        Get the best result from de pdok list (now just 1 item).
        Later we can get more than 1 item and decide which we use as best result.
        :param out: array with multiple address-items from pdok
        """
        # initial no error
        status = Errors.ERROR_GENERAL_NOER

        address_item = {}
        response = out.get("response", {})

        if response.get("numFound", 0) > 0:
            docs = response.get("docs")
            if len(docs) > 0:
                # Use the first result, this one has the highest score.
                address_item = self.to_location(docs[0])
            else:
                status = Errors.ERROR_PDOK_NO_RESU
        else:
            status = Errors.ERROR_PDOK_NO_RESU

        return status, address_item

    def to_location(self, doc_item: dict):
        """
        Translate pdok-item to location item
        :param doc_item: single pdok address
        """

        rd = (
            doc_item.get("centroide_rd", "0 0")
            .replace("POINT(", "")
            .replace(")", "")
            .split(" ")
        )
        ll = (
            doc_item.get("centroide_ll", "0 0")
            .replace("POINT(", "")
            .replace(")", "")
            .split(" ")
        )

        return {
            "latitude": float(ll[1]),
            "longitude": float(ll[0]),
            "rd_x": float(rd[0]),
            "rd_y": float(rd[1]),
            "address": doc_item.get("straatnaam", None),
            "municipality": doc_item.get("woonplaatsnaam", None),
            "zipcode": doc_item.get("postcode", None),
        }
