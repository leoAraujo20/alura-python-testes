import pytest

import requests


class TestUserOrderIntegration:
    def test_user_order_valid_user_with_services(
        self, base_urls, sample_user, sample_items, skip_if_services_down
    ):
        skip_if_services_down("order", "user")

        order_data = {"email": sample_user["email"], **sample_items}

        response = requests.post(
            f"{base_urls['order_url']}/order/create", json=order_data, allow_redirects=False
        )
        assert response.status_code == 302


    @pytest.mark.usefixtures("mock_order_service")
    def test_create_order_valid_user_mocked(self, base_urls, sample_user, sample_items):
        """Testa a criação de um pedido com usuário válido usando mock"""

        order_data = {
            "email": sample_user["email"],
            **sample_items
        }

        response = requests.post(f"{base_urls['order_url']}/create", json=order_data, allow_redirects=False)
        assert response.status_code == 302
        assert response.headers['location'] == '/order/list'


    def test_create_order_user_not_found_with_services(self, base_urls, sample_items, skip_if_services_down):
        """Testa a criação de um pedido com usuário não encontrado"""
        skip_if_services_down("order")

        order_data = {
            "user_email": "naoexiste@teste.com",
            **sample_items
        }

        response = requests.post(f"{base_urls['order_url']}/create", json=order_data, allow_redirects=False)
        assert response.status_code in [404, 400]


class TestServicesHealth:
    def test_services_health(self, services_running):
        for service, is_running in services_running.items():
            assert is_running, f"O serviço {service} não está em execução."