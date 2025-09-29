import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user(db):
    def _make(username="user", email=None, password="pass12345"):
        if email is None:
            email = f"{username}@example.com"
        user = User.objects.create_user(username=username, email=email, password=password)
        return user, password
    return _make

@pytest.fixture
def auth_client(api_client, create_user):
    """
    Returns (client, user) with Bearer token set (SimpleJWT).
    """
    def _make(username="authuser"):
        user, password = create_user(username=username)
        resp = api_client.post("/api/auth/jwt/create/", {"username": user.username, "password": password}, format="json")
        assert resp.status_code == 200, resp.content
        access = resp.data["access"]
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        return client, user
    return _make


import pytest

@pytest.fixture(autouse=True)
def no_ssl_redirect(settings):
    settings.SECURE_SSL_REDIRECT = False


import pytest

@pytest.fixture(autouse=True)
def use_in_memory_channel_layer(settings):
    """
    During tests, replace Redis channel layer with in-memory.
    """
    settings.CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer"
        }
    }
