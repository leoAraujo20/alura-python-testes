import pytest


@pytest.mark.usefixtures("db")
def test_insert_user(db):
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "password": "securepassword"
    }

    # Insert the user into the database
    db["users"].insert_one(user_data)

    # Retrieve the user from the database
    inserted_user = db["users"].find_one({"email": "test@example.com"})

    # Assert that the inserted user matches the original user data
    assert inserted_user is not None
    assert inserted_user["email"] == user_data["email"]
    assert inserted_user["name"] == user_data["name"]
    assert inserted_user["password"] == user_data["password"]