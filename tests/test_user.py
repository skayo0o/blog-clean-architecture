from fastapi.testclient import TestClient
from main import app
import uuid

client = TestClient(app)

def test_create_user():
    '''
    Тест создания пользователя.
    '''
    unique = str(uuid.uuid4())
    response = client.post("/users/", json={"username": f"testuser_{unique}", "email": f"testuser_{unique}@example.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"].startswith("testuser_")
    assert data["email"].endswith("@example.com")

def test_get_user():
    '''
    Тест получения пользователя по ID.
    '''
    unique = str(uuid.uuid4())
    response = client.post("/users/", json={"username": f"anotheruser_{unique}", "email": f"anotheruser_{unique}@example.com"})
    user_id = response.json()["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id

def test_list_users():
    '''
    Тест получения списка пользователей.
    '''
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_user():
    '''
    Тест удаления пользователя.
    '''
    response = client.post("/users/", json={"username": "todelete", "email": "todelete@example.com"})
    user_id = response.json()["id"]
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404
