import pytest
from django.contrib.auth import get_user_model

pytestmark = pytest.mark.django_db
User = get_user_model()

def _jwt_login(client, username, password):
    r = client.post("/api/auth/jwt/create/", {"username": username, "password": password}, format="json")
    assert r.status_code == 200, r.content
    return r.data["access"]

def test_like_and_unlike_flow(api_client):
    # author
    author = User.objects.create_user(username="author", email="a@x.com", password="pass12345")
    # reader
    reader = User.objects.create_user(username="reader", email="r@x.com", password="pass12345")

    # author creates a post
    token = _jwt_login(api_client, "author", "pass12345")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    post = api_client.post("/api/posts/", {"content": "post from author"}, format="json").data

    # reader likes it
    api_client.credentials()  # clear
    token2 = _jwt_login(api_client, "reader", "pass12345")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token2}")
    like_resp = api_client.post(f"/api/posts/{post['id']}/like/")
    assert like_resp.status_code in (200, 201)

    # verify list view shows liked & count=1
    list_resp = api_client.get("/api/posts/")
    assert list_resp.status_code == 200
    found = next((p for p in list_resp.data["results"] if p["id"] == post["id"]), None)
    assert found is not None
    assert found["likes_count"] == 1
    assert found["is_liked"] is True

    # unlike
    un = api_client.post(f"/api/posts/{post['id']}/unlike/")
    assert un.status_code == 204

    # verify count=0 and is_liked False
    list_resp2 = api_client.get("/api/posts/")
    found2 = next((p for p in list_resp2.data["results"] if p["id"] == post["id"]), None)
    assert found2["likes_count"] == 0
    assert found2["is_liked"] is False

def test_follow_and_unfollow(api_client):
    u1 = User.objects.create_user(username="u1", email="u1@x.com", password="pass12345")
    u2 = User.objects.create_user(username="u2", email="u2@x.com", password="pass12345")

    # login u1
    r = api_client.post("/api/auth/jwt/create/", {"username": "u1", "password": "pass12345"}, format="json")
    token = r.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    # follow u2
    r2 = api_client.post(f"/api/users/{u2.id}/follow/")
    assert r2.status_code == 201, r2.content

    # unfollow (idempotent)
    r3 = api_client.post(f"/api/users/{u2.id}/unfollow/")
    assert r3.status_code == 204
