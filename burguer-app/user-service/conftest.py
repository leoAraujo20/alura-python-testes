import os
import sys

import pytest
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


@pytest.fixture(scope="session")
def mongo_client():
    client = MongoClient(os.getenv("MONGO_URI"))
    yield client
    client.close()


@pytest.fixture(scope="function")
def db(mongo_client):
    db_name = "burguer_app_test"
    db = mongo_client[db_name]

    yield db
    db["users"].delete_many({})
    db["pedidos"].delete_many({})
