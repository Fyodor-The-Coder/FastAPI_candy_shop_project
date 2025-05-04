"""
Модуль интеграционного тестирования API Candy Shop

Пример запуска: python -m pytest tests/test_file.py

"""
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
    """Тестирование регистрации нового пользователя"""
    response = client.post("/auth/register",
                           json = {"email": client.fake_user_email,
                                   "password": client.fake_user_password,
                                   "username": client.fake_user_name}
                           )
    assert response.status_code == 200
    client.new_user_id = response.json()["user"]["id"]


def test_login():
    """Тестирование аутентификации пользователя"""
    response = client.post("/auth/login",
                           data = {"username": client.fake_user_email,
                                   "password": client.fake_user_password}
                           )
    assert response.status_code == 200
    client.auth_token = response.json()["access_token"]


def test_me():
    """Тестирование получения профиля текущего пользователя"""
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {client.auth_token}"})
    assert response.status_code == 200

    expected_data = {
        "id": client.new_user_id,
        "username": client.fake_user_name,
        "email": client.fake_user_email
    }

    assert response.json() == expected_data


def test_create_product():
    """Тестирование создания нового товара"""
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
    """Тестирование получения списка товаров"""
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
    """Тестирование получения товара по ID"""
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
    """Тестирование удаления товара"""
    response = client.delete(
        f"/products/delete_product_by_ID?product_id={client.test_product_id}",
        headers={"Authorization": f"Bearer {client.auth_token}"}
    )
    assert response.status_code == 204

    response = client.get(
        f"/products/get_product_by_ID?product_id={client.test_product_id}"
    )
    assert response.status_code == 404

def test_create_order():
    """Тестирование создания нового заказа"""
    response = client.post(
        "/orders/create_new_order",
        headers={"Authorization": f"Bearer {client.auth_token}"}
    )
    assert response.status_code == 200
    client.test_order_id = response.json()["id"]


def test_add_order_item():
    """Тестирование добавления позиции в заказ"""
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 100.0,
        "category": "Test",
        "ingredients": ["test"],
        "stock": 10
    }

    product_response = client.post(
        "/products/create_a_new_product_item",
        json=product_data,
        headers={"Authorization": f"Bearer {client.auth_token}"}
    )
    assert product_response.status_code == 201
    client.test_product_id = product_response.json()["id"]

    item_data = {"product_id": client.test_product_id, "quantity": 2}
    response = client.post(
        f"/orders/add_new_order_item?order_id={client.test_order_id}",
        json=item_data,
        headers={"Authorization": f"Bearer {client.auth_token}"}
    )
    assert response.status_code == 200
    client.test_order_item_id = response.json()["items"][0]["id"]


def test_get_all_orders():
    """Тестирование получения списка заказов"""
    response = client.get(
        "/orders/get_all_orders",
        headers={"Authorization": f"Bearer {client.auth_token}"}
    )

    assert response.status_code == 200
    orders = response.json()
    assert isinstance(orders, list)


def test_get_order_by_id():
    """Тестирование получения заказа по ID"""
    response = client.get(
        f"/orders/get_the_order_using_ID?order_id={client.test_order_id}",
        headers={"Authorization": f"Bearer {client.auth_token}"}
    )

    assert response.status_code == 200
    order = response.json()

    assert order["user_id"] == client.new_user_id

def test_remove_order_item():
    """Тестирование удаления позиции из заказа"""
    response = client.delete(
        "/orders/remove_order_item",
        params={
            "order_id": client.test_order_id,
            "item_id": client.test_order_item_id
        },
        headers={"Authorization": f"Bearer {client.auth_token}"}
    )

    assert response.status_code == 200
    assert len(response.json()["items"]) == 0
