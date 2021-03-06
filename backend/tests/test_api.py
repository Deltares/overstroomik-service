from fastapi.testclient import TestClient
from overstroomik_service.main import app


client = TestClient(app)


def test_location_lon() -> None:
    longitude = 5.0
    response = client.get("/by_location", params=dict(longitude=longitude))
    assert response.status_code == 422
    content = response.json()
    assert "detail" in content
    assert "No valid input" in content.get("detail", "")


def test_location_latlon() -> None:
    longitude = 5.0
    latitude = 53.0
    response = client.get(
        "/by_location", params=dict(longitude=longitude, latitude=latitude)
    )
    assert response.status_code == 200
    content = response.json()
    assert "location" in content


def test_location_searchfield() -> None:
    search_field = "8243LP<>'"
    response = client.get("/by_location", params=dict(search_field=search_field))
    assert response.status_code == 200
    content = response.json()
    assert "location" in content
    assert (
        content.get("location", {}).get("search_field")
        == "8243LP&amp;lt;&amp;gt;&amp;#x27;"
    )
