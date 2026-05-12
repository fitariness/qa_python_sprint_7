"""Принятие заказа: успех, ошибки при отсутствии или неверных id курьера и заказа.

Кейсы без реального заказа идут через фикстуру courier_only, чтобы не дергать GET /orders/track сразу после создания
"""

import allure
from http import HTTPStatus

from helpers.api_docs import (
    MSG_ACCEPT_COURIER_ID_NOT_EXISTS,
    MSG_ACCEPT_ORDER_ID_NOT_EXISTS,
    MSG_HTTP_NOT_FOUND_DOT,
    MSG_SEARCH_INSUFFICIENT,
)
from helpers.order_helpers import accept_order


@allure.feature("Orders")
@allure.story("Принять заказ")
class TestAcceptOrder:
    @allure.title("Успешное принятие: ok: true")
    def test_success_returns_ok_true(self, courier_and_order):
        steps = courier_and_order
        response = accept_order(steps["order_id"], steps["courier_id"])
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {"ok": True}

    @allure.title("Без courierId - 400")
    def test_missing_courier_id_returns_error(
        self, courier_and_order, orders_api_client
    ):
        order_id = courier_and_order["order_id"]
        response = orders_api_client.accept(order_id)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json().get("message") == MSG_SEARCH_INSUFFICIENT

    @allure.title("Неверный id курьера - 404")
    def test_wrong_courier_id_returns_error(self, courier_and_order, orders_api_client):
        order_id = courier_and_order["order_id"]
        response = orders_api_client.accept(order_id, courier_id=999_999_999)
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json().get("message") == MSG_ACCEPT_COURIER_ID_NOT_EXISTS

    @allure.title("Без id заказа в пути - 404 Not Found")
    def test_missing_order_id_returns_error(self, courier_only, orders_api_client):
        courier_id = courier_only["id"]
        response = orders_api_client.accept(order_id=None, courier_id=courier_id)
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json().get("message") == MSG_HTTP_NOT_FOUND_DOT

    @allure.title("Неверный id заказа - 404")
    def test_wrong_order_id_returns_error(self, courier_only):
        courier_id = courier_only["id"]
        response = accept_order(999_999_999, courier_id)
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json().get("message") == MSG_ACCEPT_ORDER_ID_NOT_EXISTS
