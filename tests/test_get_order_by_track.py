"""Заказ по треку: успех, запрос без номера, несуществующий номер."""

import allure
from http import HTTPStatus

from helpers.api_docs import MSG_ORDER_NOT_FOUND, MSG_SEARCH_INSUFFICIENT
from helpers.order_helpers import get_order_by_track


@allure.feature("Orders")
@allure.story("Получить заказ по номеру")
class TestGetOrderByTrack:
    @allure.title("Успешный запрос возвращает объект заказа")
    def test_success_returns_order_object(self, created_order_track):
        track = created_order_track
        response = get_order_by_track(track)
        assert response.status_code == HTTPStatus.OK
        response_json = response.json()
        assert "order" in response_json
        order = response_json["order"]
        assert isinstance(order, dict)
        assert order.get("track") == track

    @allure.title("Без номера заказа - ошибка")
    def test_without_track_returns_error(self, orders_api_client):
        response = orders_api_client.track()
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json().get("message") == MSG_SEARCH_INSUFFICIENT

    @allure.title("Несуществующий track - 404, заказ не найден")
    def test_nonexistent_track_returns_not_found(self, orders_api_client):
        response = orders_api_client.track(999_999_999)
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json().get("message") == MSG_ORDER_NOT_FOUND
