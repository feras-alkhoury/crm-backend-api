from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def get_token():
    client.post(
        "/auth/register",
        json={
            "username": "feras",
            "password": "Test12345",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "feras",
            "password": "Test12345",
        },
    )

    print("LOGIN:", response.status_code, response.json())

    assert response.status_code == 200

    return response.json()["access_token"]


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "CRM Backend API is running"



def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_register():    response = client.post(
        "/auth/register",
        json={
            "username": "test_user",
            "password": "Test12345",
        },
    )

    assert response.status_code in (200, 400)


def test_login():
    token = get_token()

    assert token


def test_customers_requires_authentication():
    response = client.get("/customers")

    assert response.status_code == 401


def test_create_customer():
    token = get_token()

    response = client.post(
        "/customers",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Test Customer",
            "email": "test.customer@example.com",
            "phone": "123456789",
            "company": "Test Company",
        },
    )

    assert response.status_code in (201, 400)

    if response.status_code == 201:
        data = response.json()
        assert data["name"] == "Test Customer"
        assert data["email"] == "test.customer@example.com"


def test_get_customers():
    token = get_token()

    response = client.get(
        "/customers",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_search_customers():
    token = get_token()

    response = client.get(
        "/customers?search=Test",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_pagination():
    token = get_token()

    response = client.get(
        "/customers?skip=0&limit=10",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_customer_by_id():
    token = get_token()

    response = client.get(
        "/customers/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code in (200, 404)


def test_update_customer():
    token = get_token()

    response = client.put(
        "/customers/1",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Updated Customer",
            "email": "updated.customer@example.com",
            "phone": "987654321",
            "company": "Updated Company",
        },
    )

    assert response.status_code in (200, 404)


def test_delete_customer():
    token = get_token()

    response = client.delete(
        "/customers/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code in (200, 404)
