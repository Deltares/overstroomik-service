"""
This class uses the pdok-api to find address information

"""

import httpx
from overstroomik_service.auto_models import Location

ERROR_GENERAL_NOER = "no-error"
ERROR_PDOK_NO_RESP = "Geen response PDOK"
ERROR_PDOK_NO_RESU = "Geen eenduidige resultaat PDOK"
ERROR_GENERAL_ERRO = "Service niet bereikbaar"


class PDOK():

    # pdok api url
    api = "https://geodata.nationaalgeoregister.nl/locatieserver/v3/free"

    # fields we need
    fields = "centroide_rd,centroide_ll,straatnaam,woonplaatsnaam,postcode"

    async def address_by_search_field(self, search_field: str):
        """
        Search address information with specified search string.
        :param search_field: content of original search field
        """

        # build api_url
        url = f"{self.api}?q={search_field}&rows=1&fl={self.fields}"

        # fetch date and return address
        status, address_item = await self.fetch_data(url)
        address_item["search_field"] = search_field

        return status, Location(**address_item)

    async def address_by_latlon(self, latitude: float, longitude: float):
        """
        Search address information with specified latitude and longitude.
        :param latitude: coordinate in degrees in EPSG:4326
        :param longitude: coordinate in degrees in EPSG:4326
        """

        # build api_url
        url = f"{self.api}?q=type:adres&lat={latitude}&lon={longitude}&rows=1&fl={self.fields}"

        # fetch date and return address
        status, address_item = await self.fetch_data(url)

        return status, Location(**address_item)

    async def fetch_data(self, url: str):
        """
        Get the data from PDOK
        :param url: api url to fetch
        """

        # connect async to the pdok-api
        async with httpx.AsyncClient() as client:
            result = await client.get(url, timeout=10.0)

            if result.status_code == httpx.codes.OK:
                status, address_item = self.list_to_location(result.json())
            else:
                status = ERROR_PDOK_NO_RESP

        # return status and address information
        return status, address_item

    def list_to_location(self, out: dict):
        """
        Get the best result from de pdok list (now just 1 item).
        Later we can get more than 1 item and decide which we use as best result.
        :param out: array with multiple address-items from pdok
        """
        # initial no error
        status = ERROR_GENERAL_NOER

        address_item = {}
        response = out.get("response")

        if response.get("numFound", 0) > 0:
            docs = response.get("docs")
            if len(docs) > 0:
                # Use the first result, this one has the highest score.
                address_item = self.to_location(docs[0])
            else:
                status = ERROR_PDOK_NO_RESU
        else:
            status = ERROR_PDOK_NO_RESU

        return status, address_item

    def to_location(self, doc_item: dict):
        """
        Translate pdok-item to location item
        :param doc_item: single pdok address
        """

        rd = doc_item.get("centroide_rd", "0 0").replace("POINT(",
                                                         "").replace(")", "").split(" ")
        ll = doc_item.get("centroide_ll", "0 0").replace("POINT(",
                                                         "").replace(")", "").split(" ")

        return {
            "latitude": float(ll[1]),
            "longitude": float(ll[0]),
            "rd_x": float(rd[0]),
            "rd_y": float(rd[1]),
            "address": doc_item.get("straatnaam", None),
            "municipality": doc_item.get("woonplaatsnaam", None),
            "zipcode": doc_item.get("postcode", None),
        }
