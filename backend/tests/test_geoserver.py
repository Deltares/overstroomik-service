import os
import pytest
import asyncio
from overstroomik_service.errors import Errors
from overstroomik_service.geoserver import Geoserver
from overstroomik_service.config import settings
import warnings


@pytest.mark.skipif(
    (not settings.COMPOSE),
    reason="requires geoserver with docker-compose (see COMPOSE env)",
)
@pytest.mark.asyncio
async def test_get_data() -> None:
    """
    Test a valid situation with expected values
    """

    status, data = await Geoserver.get_data(
        rd_x=158492.416, rd_y=502424.151, geoserver_url=settings.GEOSERVER_URL,
    )

    assert status == Errors.ERROR_GENERAL_NOER
    assert data.flood_type == "binnen dijkring, mogelijk overstroombaar"
    assert data.maximum_water_depth == 2.0899999141693115
    assert data.probability_of_flooding is None
    assert data.evacuation_percentage == 55
    assert data.safety_board_id == 25


@pytest.mark.asyncio
async def test_no_service() -> None:
    """
    Test when the geoserver in unavailable
    """
    status, data = await Geoserver.get_data(
        rd_x=158492.416,
        rd_y=502424.151,
        geoserver_url=f"http://non-existent:8080/geoserver",
    )

    assert status == Errors.ERROR_GEOS_NO_RESP


@pytest.mark.skipif(
    (not settings.COMPOSE),
    reason="requires geoserver with docker-compose (see COMPOSE env)",
)
def test_get_api_url_from_rd() -> None:
    """
    Test the creation of the api url, it return also the width, height, x and x.
    Input rd_x and rd_y is different
    """

    # test 1
    # Given the x and y, this must result a valid coordinate with the specific values
    api_url, coordinate_is_valid, indices = Geoserver.get_api_url_from_rd(
        rd_x=158492.416, rd_y=502424.151, geoserver_url=settings.GEOSERVER_URL,
    )

    assert settings.GEOSERVER_URL in api_url
    assert indices[2] == 157858.416
    assert indices[3] == 134556.849
    assert indices[0] == 283666.0
    assert indices[1] == 330387.0
    assert coordinate_is_valid is True

    # test 2
    # Given the x and y, this must result a invalid coordinate with no values
    # The input is outside the grouplayers extend
    api_url, coordinate_is_valid, indices = Geoserver.get_api_url_from_rd(
        rd_x=633, rd_y=636982, geoserver_url=settings.GEOSERVER_URL
    )

    assert settings.GEOSERVER_URL in api_url
    assert indices[2] == -1
    assert indices[3] == -1
    assert coordinate_is_valid is False

    # test 3
    # Given the x and y, this must result a invalid coordinate with no values
    # The input is outside the grouplayers extend
    api_url, coordinate_is_valid, indices = Geoserver.get_api_url_from_rd(
        rd_x=284301, rd_y=306594, geoserver_url=settings.GEOSERVER_URL,
    )

    assert settings.GEOSERVER_URL in api_url
    assert indices[2] == 284301 - 634
    assert indices[3] == 636981 - 306594
    assert coordinate_is_valid is False
