from fastapi.testclient import TestClient
import faker
from app.main import app

client = TestClient(app)
fake = faker.Faker()

client.fake_user_email = fake.email()
client.fake_user_password = fake.password()
client.fake_user_name = fake.first_name()
client.new_user_id = 0
client.auth_token = ""

def test_register():
    response = client.post("/auth/register",
                           json = {"email": client.fake_user_email,
                                   "password": client.fake_user_password,
                                   "username": client.fake_user_name}
                           )
    assert response.status_code == 200
    client.new_user_id = response.json()["user"]["id"]


def test_login():
    response = client.post("/auth/login",
                           data = {"username": client.fake_user_email,
                                   "password": client.fake_user_password}
                           )
    assert response.status_code == 200
    client.auth_token = response.json()["access_token"]


def test_me():
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {client.auth_token}"})
    assert response.status_code == 200

    expected_data = {
        "id": client.new_user_id,
        "username": client.fake_user_name,
        "email": client.fake_user_email
    }

    assert response.json() == expected_data


def test_create_product():
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 100.50,
        "category": "Test Category",
        "ingredients": ["ingredient1", "ingredient2"],
        "stock": 10
    }

    response = client.post(
        "/products/create_a_new_product_item",
        json=product_data,
        headers={"Authorization": f"Bearer {client.auth_token}"}
    )

    assert response.status_code == 201
    created_product = response.json()

    client.test_product_id = created_product["id"]
    client.test_product_data = product_data

    assert "id" in created_product
    assert created_product["name"] == product_data["name"]
    assert created_product["price"] == product_data["price"]


def test_get_all_products():
    response = client.get("/products/view_all_products")
    assert response.status_code == 200

    products = response.json()
    assert isinstance(products, list)

    found = any(p["id"] == client.test_product_id for p in products)
    assert found is True

    first_product = products[0]
    assert "id" in first_product
    assert "name" in first_product
    assert "price" in first_product
    assert "stock" in first_product
    assert "description" not in first_product


def test_get_product_by_id():
    response = client.get(
        f"/products/get_product_by_ID?product_id={client.test_product_id}"
    )
    assert response.status_code == 200
    product = response.json()

    assert product["id"] == client.test_product_id
    assert product["description"] == client.test_product_data["description"]
    assert product["category"] == client.test_product_data["category"]

    response = client.get("/products/get_product_by_ID?product_id=999999")
    assert response.status_code == 404

def test_delete_product():
    response = client.delete(
        f"/products/delete_product_by_ID?product_id={client.test_product_id}",
        headers={"Authorization": f"Bearer {client.auth_token}"}
    )
    assert response.status_code == 204

    response = client.get(
        f"/products/get_product_by_ID?product_id={client.test_product_id}"
    )
    assert response.status_code == 404
