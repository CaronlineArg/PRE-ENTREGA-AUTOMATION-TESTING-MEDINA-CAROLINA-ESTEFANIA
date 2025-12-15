import pytest
import requests

from utils.logger import get_logger

logger = get_logger("API_TESTS")


BASE = "https://jsonplaceholder.typicode.com"


@pytest.mark.api
def test_get_users():
    r = requests.get(f"{BASE}/users")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.api
def test_create_user():
    payload = {"name": "Carolina QA", "job": "tester"}

    r = requests.post(f"{BASE}/posts", json=payload)
    assert r.status_code == 201

    body = r.json()
    assert body["name"] == payload["name"]


@pytest.mark.api
def test_delete_user():
    r = requests.delete(f"{BASE}/posts/1")
    assert r.status_code in [200, 204]

@pytest.mark.api
def test_get_user_not_found():
    r = requests.get("https://jsonplaceholder.typicode.com/users/9999")

    assert r.status_code == 404

#encadenamiento de requests
@pytest.mark.api
def test_create_post_only():
    payload = {"title": "QA Test", "body": "Encadenado", "userId": 1}
    post = requests.post("https://jsonplaceholder.typicode.com/posts", json=payload)

    assert post.status_code == 201
    data = post.json()
    assert data["title"] == payload["title"]
