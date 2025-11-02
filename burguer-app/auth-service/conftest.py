import pytest
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope="session")
def mongo_client():
    mongo_uri = os.getenv("MONGO_URI")
    client = MongoClient(mongo_uri)
    yield client
    client.close()


@pytest.fixture(scope="function")
def db(mongo_client):
    db_name = "burguer_app_test"
    db = mongo_client[db_name]

    yield db
    db["users"].delete_many({})
    db["pedidos"].delete_many({})