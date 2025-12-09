import pytest
import requests

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
