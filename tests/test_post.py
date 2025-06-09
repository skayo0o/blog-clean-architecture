from fastapi.testclient import TestClient
from main import app
import uuid

client = TestClient(app)

def create_user():
    '''
    Создание тестового пользователя для постов.
    '''
    unique = str(uuid.uuid4())
    response = client.post("/users/", json={
        "username": f"postuser_{unique}",
        "email": f"postuser_{unique}@example.com"
    })
    return response.json()["id"]

def test_create_post():
    '''
    Тест создания поста.
    '''
    author_id = create_user()
    response = client.post("/posts/", json={
        "title": "Test Post",
        "content": "Post content",
        "author_id": author_id,
        "tags": ["tag1", "tag2"]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Post"
    assert data["author_id"] == author_id

def test_get_post():
    '''
    Тест получения поста по ID.
    '''
    author_id = create_user()
    response = client.post("/posts/", json={
        "title": "Get Post",
        "content": "Content",
        "author_id": author_id,
        "tags": []
    })
    post_id = response.json()["id"]
    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == post_id

def test_list_posts():
    '''
    Тест получения списка постов.
    '''
    response = client.get("/posts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_post():
    '''
    Тест удаления поста.
    '''
    author_id = create_user()
    response = client.post("/posts/", json={
        "title": "Delete Post",
        "content": "Content",
        "author_id": author_id,
        "tags": []
    })
    post_id = response.json()["id"]
    response = client.delete(f"/posts/{post_id}")
    assert response.status_code == 204
    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 404
