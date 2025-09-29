import pytest

pytestmark = pytest.mark.django_db

def test_create_post_requires_auth(api_client):
    r = api_client.post("/api/posts/", {"content": "hi"}, format="json")
    assert r.status_code in (401, 403)

def test_create_post_ok(auth_client):
    client, user = auth_client(username="writer")
    r = client.post("/api/posts/", {"content": "hello world"}, format="json")
    assert r.status_code == 201, r.content
    assert r.data["content"] == "hello world"
    assert r.data["author"]["username"] == "writer"

def test_list_posts_shows_counts(auth_client):
    client, user = auth_client(username="writer2")
    client.post("/api/posts/", {"content": "one"}, format="json")
    r = client.get("/api/posts/")
    assert r.status_code == 200
    assert r.data["count"] >= 1
    first = r.data["results"][0]
    assert "likes_count" in first and "comments_count" in first
