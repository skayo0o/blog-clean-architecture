from fastapi.testclient import TestClient
from main import app
import uuid

client = TestClient(app)

def create_user():
    unique = str(uuid.uuid4())
    response = client.post("/users/", json={
        "username": f"commentuser_{unique}",
        "email": f"commentuser_{unique}@example.com"
    })
    return response.json()["id"]

def create_post(author_id):
    response = client.post("/posts/", json={
        "title": "Comment Post",
        "content": "Content",
        "author_id": author_id,
        "tags": []
    })
    return response.json()["id"]

def test_create_comment():
    author_id = create_user()
    post_id = create_post(author_id)
    response = client.post("/comments/", json={
        "post_id": post_id,
        "author_id": author_id,
        "content": "Nice post!",
        "parent_comment_id": None
    })
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Nice post!"
    assert data["post_id"] == post_id

def test_get_comment():
    author_id = create_user()
    post_id = create_post(author_id)
    response = client.post("/comments/", json={
        "post_id": post_id,
        "author_id": author_id,
        "content": "Get comment",
        "parent_comment_id": None
    })
    comment_id = response.json()["id"]
    response = client.get(f"/comments/{comment_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == comment_id

def test_list_comments():
    author_id = create_user()
    post_id = create_post(author_id)
    client.post("/comments/", json={
        "post_id": post_id,
        "author_id": author_id,
        "content": "List comment",
        "parent_comment_id": None
    })
    response = client.get(f"/comments/?post_id={post_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_comment():
    author_id = create_user()
    post_id = create_post(author_id)
    response = client.post("/comments/", json={
        "post_id": post_id,
        "author_id": author_id,
        "content": "To delete",
        "parent_comment_id": None
    })
    comment_id = response.json()["id"]
    response = client.delete(f"/comments/{comment_id}")
    assert response.status_code == 204
    response = client.get(f"/comments/{comment_id}")
    assert response.status_code == 404