"""Список заказов: в JSON ответе - массив заказов; ошибка при несуществующем courierId."""

import allure
from http import HTTPStatus

from helpers.api_docs import courier_not_found_message


@allure.feature("Orders")
@allure.story("Список заказов")
class TestOrdersList:
    @allure.title("В ответе возвращается список заказов")
    def test_response_contains_orders_list(self, orders_api_client):
        response = orders_api_client.list_orders()
        assert response.status_code == HTTPStatus.OK
        response_json = response.json()
        assert "orders" in response_json
        assert isinstance(response_json["orders"], list)

    @allure.title("Несуществующий courierId - 404 и сообщение")
    def test_unknown_courier_id_returns_not_found(self, orders_api_client):
        fake_id = 999_999_999
        response = orders_api_client.list_orders(courierId=fake_id)
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json().get("message") == courier_not_found_message(fake_id)
