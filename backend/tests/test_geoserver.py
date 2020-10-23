import pytest
import asyncio
from overstroomik_service.geoserver import Geoserver
import warnings


async def test_get_data() -> None:
    geoserver = Geoserver()
    status, data = await geoserver.get_data(
        rd_x=158492.416,
        rd_y=502424.151,
        geoserver_url="http://localhost:8080/geoserver")

    assert status == "no-error"
    assert data.flood_type == "binnen dijkring, mogelijk overstroombaar"
    assert data.maximum_water_depth == 2.0899999141693115
    assert data.probability_of_flooding is None
    assert data.evacuation_percentage == 55
    assert data.safety_board_id == 25


def test_get_api_url_from_rd() -> None:
    # test 1
    geoserver = Geoserver()
    data = geoserver.get_api_url_from_rd(
        rd_x=158492.416,
        rd_y=502424.151,
        geoserver_url="http://localhost:8080/geoserver")

    assert "http://localhost:8080/geoserver" in data.get("api_url", "")
    assert data.get("x", 0) == 157858.416
    assert data.get("y", 0) == 134556.849
    assert data.get("width", 0) == 283666.0
    assert data.get("height", 0) == 330387.0
    assert data.get("valid", False) is True

    # test 2
    data = geoserver.get_api_url_from_rd(
        rd_x=633,
        rd_y=636982,
        geoserver_url="http://localhost:8080/geoserver")

    assert "http://localhost:8080/geoserver" in data.get("api_url", "")
    assert data.get("x", 0) == -1
    assert data.get("y", 0) == -1
    assert data.get("valid", True) is False

    # test 3
    data = geoserver.get_api_url_from_rd(
        rd_x=284301,
        rd_y=306594,
        geoserver_url="http://localhost:8080/geoserver")

    assert "http://localhost:8080/geoserver" in data.get("api_url", "")
    assert data.get("x", 0) == 284301 - 634
    assert data.get("y", 0) == 636981 - 306594
    assert data.get("valid", True) is False
