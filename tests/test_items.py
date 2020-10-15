from fastapi.testclient import TestClient
from overstroomik_service.main import app


client = TestClient(app)


def test_read_item() -> None:
    response = client.get("/items/1")
    assert response.status_code == 200
    content = response.json()
    assert "item_id" in content
