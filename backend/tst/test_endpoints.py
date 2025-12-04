from fastapi.testclient import TestClient
from src.main import app
import time

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_cpu_task():
    start = time.time()
    response = client.get("/run/backendCPUExpensiveTask/1")
    duration = time.time() - start
    assert response.status_code == 200
    assert duration >= 1

def test_io_task():
    start = time.time()
    response = client.get("/run/backendIoContentionTask/1")
    duration = time.time() - start
    assert response.status_code == 200
    assert duration >= 1

# DB tests might fail if DB is not running. 
# We can mock the DB session or just skip if connection fails.
# For now, let's try to run them and see.
