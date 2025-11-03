import os
from unittest.mock import Mock, patch

import pytest
import requests
from dotenv import load_dotenv
from pymongo import MongoClient

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


@pytest.fixture
def base_urls():
    return {
        "auth_url": "http://localhost:5000/",
        "user_url": "http://localhost:5001/",
        "order_url": "http://localhost:5002/",
        "product_url": "http://localhost:5003/",
    }


@pytest.fixture
def sample_user():
    return {
        "email": "test@example.com",
        "name": "Test User",
        "address": "123 Test St, Test City, TX",
        "role": "cliente",
    }


@pytest.fixture
def sample_items():
    return {
        "item_name": ["Hambúrguer Teste", "Refrigerante Teste"],
        "item_price": [10.0, 5.0],
        "quantity": ["2", "1"],
    }


@pytest.fixture
def mock_user_service():
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "email": "cliente@teste.com",
            "name": "Cliente Teste",
            "address": "Rua Teste, 123",
            "role": "cliente",
        }
        mock_get.return_value = mock_response
        yield mock_get


@pytest.fixture
def mock_order_service():
    with patch("requests.post") as mock_post:
        mock_response = Mock()
        mock_response.status_code = 302
        mock_response.headers = {"location": "/order/list"}
        mock_post.return_value = mock_response
        yield mock_post


def check_service_health(url):
    try:
        response = requests.get(f"{url}/", timeout=2)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


@pytest.fixture
def services_running(base_urls):
    return {service: check_service_health(url) for service, url in base_urls.items()}


@pytest.fixture
def skip_if_services_down(services_running):
    """Pula testes se os serviços não estiverem rodando"""
    def _skip_if_down(*required_services):
        for service in required_services:
            if not services_running.get(f"{service}_url", False):
                pytest.skip(f"Serviço {service} não está rodando")
    return _skip_if_down
