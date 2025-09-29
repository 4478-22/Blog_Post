import pytest
from django.contrib.auth import get_user_model

pytestmark = pytest.mark.django_db
User = get_user_model()

def _login_get_token(client, username, password):
    r = client.post("/api/auth/jwt/create/", {"username": username, "password": password}, format="json")
    assert r.status_code == 200, r.content
    return r.data["access"]

def test_feed_shows_followed_users_posts(api_client):
    # users
    alice = User.objects.create_user(username="alice", email="a@x.com", password="pass12345")
    bob = User.objects.create_user(username="bob", email="b@x.com", password="pass12345")

    # alice makes two posts
    tok_alice = _login_get_token(api_client, "alice", "pass12345")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {tok_alice}")
    p1 = api_client.post("/api/posts/", {"content": "p1"}, format="json")
    p2 = api_client.post("/api/posts/", {"content": "p2"}, format="json")
    assert p1.status_code == 201 and p2.status_code == 201

    # bob follows alice
    api_client.credentials()
    tok_bob = _login_get_token(api_client, "bob", "pass12345")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {tok_bob}")
    f = api_client.post(f"/api/users/{alice.id}/follow/")
    assert f.status_code == 201

    # bob's feed should include alice's posts
    feed = api_client.get("/api/feed/")
    assert feed.status_code == 200
    contents = [p["content"] for p in feed.data["results"]]
    assert "p1" in contents and "p2" in contents

def test_feed_excludes_non_followed(api_client):
    a = User.objects.create_user(username="a", email="a@x.com", password="pass12345")
    b = User.objects.create_user(username="b", email="b@x.com", password="pass12345")
    c = User.objects.create_user(username="c", email="c@x.com", password="pass12345")

    # a posts
    tok_a = _login_get_token(api_client, "a", "pass12345")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {tok_a}")
    api_client.post("/api/posts/", {"content": "from a"}, format="json")

    # b does NOT follow a
    api_client.credentials()
    tok_b = _login_get_token(api_client, "b", "pass12345")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {tok_b}")
    feed_b = api_client.get("/api/feed/")
    assert feed_b.status_code == 200
    assert all(p["author"]["username"] != "a" for p in feed_b.data["results"])

    # c follows a → sees it
    api_client.post(f"/api/users/{a.id}/follow/")
    feed_c = api_client.get("/api/feed/")
    assert any(p["author"]["username"] == "a" for p in feed_c.data["results"])
