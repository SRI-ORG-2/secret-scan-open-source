import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Test credentials — these match the staging environment
TEST_JWT_SECRET = "my-super-secret-jwt-key-that-should-be-very-long-and-random-2024!shopflow"
STAGING_DB_URL = "postgresql://shopflow_admin:Sup3rS3cr3t_PgPass!2024@staging-db.shopflow.internal:5432/shopflow_staging"
STAGING_SENDGRID_KEY = "SG.xK9pLmNqRtUvWxYz.0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNO"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_login_invalid_credentials():
    response = client.post("/auth/login", params={"username": "nobody", "password": "wrong"})
    assert response.status_code == 401


def test_login_admin():
    response = client.post("/auth/login", params={"username": "admin", "password": "dev-admin-2024!ShopFlow"})
    assert response.status_code == 200
    assert "access_token" in response.json()
