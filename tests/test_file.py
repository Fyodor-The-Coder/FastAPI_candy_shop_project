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

