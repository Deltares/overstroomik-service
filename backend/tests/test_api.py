from fastapi.testclient import TestClient
from overstroomik_service.main import app


client = TestClient(app)


def test_location() -> None:
    longitude = 5.0
    response = client.get("/by_location", params=dict(longitude=longitude))
    assert response.status_code == 200
    content = response.json()
    assert "location" in content
    assert content.get("location", {}).get("longitude") == longitude
