import pytest
import asyncio
from overstroomik_service.errors import Errors
from overstroomik_service.pdok import PDOK
import warnings


async def test_address_by_search_field() -> None:
    pdok = PDOK()
    status, location = await pdok.address_by_search_field(search_field="8232JN")

    assert status == Errors.ERROR_GENERAL_NOER
    assert location.latitude == 52.50669969
    assert location.longitude == 5.46887432
    assert location.rd_x == 160544.902
    assert location.rd_y == 502115.495
    assert location.search_field == "8232JN"
    assert location.address == "Botter 11"
    assert location.municipality == "Lelystad"
    assert location.zipcode == "8232JN"


async def test_address_by_latlon() -> None:
    pdok = PDOK()
    status, location = await pdok.address_by_latlon(latitude=52.50669969, longitude=5.46887432)

    assert status == Errors.ERROR_GENERAL_NOER
    assert location.latitude == 52.50669597
    assert location.longitude == 5.46888296
    assert location.rd_x == 160545.489
    assert location.rd_y == 502115.081
    assert location.search_field is None
    assert location.address == "Botter 11"
    assert location.municipality == "Lelystad"
    assert location.zipcode == "8232JN"


async def test_fetch_data() -> None:
    pdok = PDOK()

    api = "https://geodata.nationaalgeoregister.nl/locatieserver/v3/free"
    fields = "centroide_rd,centroide_ll,straatnaam,woonplaatsnaam,postcode"

    latitude = 52.50669969
    longitude = 5.46887432

    url = f"{api}?q=type:adres&lat={latitude}&lon={longitude}&rows=1&fl={fields}"
    status, adress_item = await pdok.fetch_data(url=url)

    assert status == Errors.ERROR_GENERAL_NOER
    assert adress_item.get("latitude", 0) == 52.50669597
    assert adress_item.get("longitude", 0) == 5.46888296
    assert adress_item.get("address", "") == "Botter 11"
    assert adress_item.get("municipality", "") == "Lelystad"
    assert adress_item.get("zipcode", "") == "8232JN"


def test_list_to_location() -> None:

    pdok_result = {
        "response": {
            "numFound": 9395778,
            "start": 0,
            "maxScore": 0.17737934,
            "docs": [
                {
                    "woonplaatsnaam": "Lelystad",
                    "postcode": "8232JN",
                    "centroide_ll": "POINT(5.46888296 52.50669597)",
                    "centroide_rd": "POINT(160545.489 502115.081)",
                    "straatnaam": "Botter 11",
                }
            ]
        }
    }

    pdok = PDOK()
    status, adress_item = pdok.list_to_location(out=pdok_result)

    assert status == Errors.ERROR_GENERAL_NOER
    assert adress_item.get("latitude", 0) == 52.50669597
    assert adress_item.get("longitude", 0) == 5.46888296
    assert adress_item.get("rd_x", 0) == 160545.489
    assert adress_item.get("rd_y", 0) == 502115.081
    assert adress_item.get("address", "") == "Botter 11"
    assert adress_item.get("municipality", "") == "Lelystad"
    assert adress_item.get("zipcode", "") == "8232JN"


def test_to_location() -> None:

    doc_item = {
        "woonplaatsnaam": "Lelystad",
        "postcode": "8232JN",
        "centroide_ll": "POINT(5.46888296 52.50669597)",
        "centroide_rd": "POINT(160545.489 502115.081)",
        "straatnaam": "Botter 11"
    }

    pdok = PDOK()
    adress_item = pdok.to_location(doc_item=doc_item)

    assert adress_item.get("latitude", 0) == 52.50669597
    assert adress_item.get("longitude", 0) == 5.46888296
    assert adress_item.get("rd_x", 0) == 160545.489
    assert adress_item.get("rd_y", 0) == 502115.081
    assert adress_item.get("address", "") == "Botter 11"
    assert adress_item.get("municipality", "") == "Lelystad"
    assert adress_item.get("zipcode", "") == "8232JN"
