from fastapi.testclient import TestClient
from overstroomik_service.main import app


client = TestClient(app)


def test_location() -> None:
    longitude = 5.0
    response = client.get("/by_location", params=dict(longitude=longitude))
    assert response.status_code == 422
    content = response.json()
    assert "location" in content
    assert content.get("location", {}).get("longitude") == longitude


def test_location() -> None:
    search_field = "8243LP<>'"
    response = client.get("/by_location", params=dict(search_field=search_field))
    assert response.status_code == 200
    content = response.json()
    assert "location" in content
    assert (
        content.get("location", {}).get("search_field")
        == "8243LP&amp;lt;&amp;gt;&amp;#x27;"
    )
