from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_print_routes():
    for route in app.routes:
        print(route.path)
    assert True

def test_health():
    response = client.get("/")
    assert response.status_code == 200

def test_user_register():
    response = client.post("/auth/signup", json={
        "email": "test@example.com",
        "password": "test123"
    })
    assert response.status_code in [200, 400]

def test_login():
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "test123"
    })
    assert response.status_code in [200, 401]

