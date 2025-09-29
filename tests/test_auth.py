import pytest

pytestmark = pytest.mark.django_db


def test_registration_creates_user_and_profile(api_client):
    payload = {"username": "alice", "email": "a@x.com", "password": "passw0rd123"}
    r = api_client.post("/api/auth/register/", payload, format="json")  # ✅ note trailing slash

    # Debugging output (won’t break test, just helps us see why it failed)
    print("Status:", r.status_code)
    print("Headers:", dict(r.headers))

    # Explicitly fail if we hit a redirect
    if r.status_code in (301, 302):
        pytest.fail(f"Got redirect to {r.headers.get('Location')} instead of 201")

    assert r.status_code == 201, r.content
    assert r.data["username"] == "alice"
    assert "profile" in r.data


def test_jwt_login(api_client, create_user):
    user, password = create_user(username="bob")
    r = api_client.post("/api/auth/jwt/create/", {"username": user.username, "password": password}, format="json")
    assert r.status_code == 200, r.content
    assert "access" in r.data and "refresh" in r.data
