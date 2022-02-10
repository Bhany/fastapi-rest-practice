from fastapi.testclient import TestClient
import sys
sys.path.insert(0, '../')

from main import app

client = TestClient(app)

def test_aggregate_node_weights_unit():
    response = client.get("/nodes/aggregate/kg/")
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid weight unit:'kg'"}
