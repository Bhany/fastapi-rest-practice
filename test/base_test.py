from fastapi.testclient import TestClient
import sys
sys.path.insert(0, '../')

from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"hello": "world"}
