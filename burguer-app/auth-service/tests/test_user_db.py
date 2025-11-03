import pytest


@pytest.mark.usefixtures("db")
def test_insert_user(db):
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "password": "securepassword"
    }

    db["users"].insert_one(user_data)

    inserted_user = db["users"].find_one({"email": "test@example.com"})

    assert inserted_user is not None
    assert inserted_user["email"] == user_data["email"]
    assert inserted_user["name"] == user_data["name"]
    assert inserted_user["password"] == user_data["password"]