from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_fail_register():

    res = client.post(
        "/register",
        json={
            "username": "pariya20",
            "email": "py@kk.com",
            "password": "1234000"
        }
    )

    assert res.status_code == 409


def test_success_register():

    res = client.post(
        "/register",
        json={
            "username": "pariya_test_500",
            "email": "pariya_test_500@gmail.com",
            "password": "1234000"
        }
    )

    assert res.status_code == 200



def test_login():

    res = client.post(
        "/login",
        json={
            "username": "pariya_test_500",
            "email": "pariya_test_500@gmail.com",
            "password": "1234000"
        }
    )

    assert res.status_code == 200


def test_get_pro():

    res = client.get("/products")

    assert res.status_code == 200


def test_get_product_not_found():

    response = client.get("/products/999999")

    assert response.status_code == 404


def test_product_search():

    response = client.get(
        "/products?search=laptop"
    )

    assert response.status_code == 200


def test_product_price_filter():

    response = client.get(
        "/products?min_price=100&max_price=1000"
    )

    assert response.status_code == 200


def test_create_customer():

    response = client.post(
        "/customers",
        json={
            "name": "Test Customer",
            "phone": "09123456789",
            "email": "customer@test.com",
            "address": "Test Address"
        }
    )

    assert response.status_code == 200


def test_get_customers():

    response = client.get("/customers")

    assert response.status_code == 200