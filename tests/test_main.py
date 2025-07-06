from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient):
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Bem-vindo ao Aurora Core" in data["message"]