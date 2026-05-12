"""Создание заказа: варианты цвета (параметризация), наличие track в ответе."""

import allure
import pytest
from http import HTTPStatus

from helpers.order_helpers import create_order
from testdata.orders import CREATE_ORDER_COLOR_PARAMS


@allure.feature("Orders")
@allure.story("Создание заказа")
class TestCreateOrder:
    @pytest.mark.parametrize("color_fields", CREATE_ORDER_COLOR_PARAMS)
    @allure.title("Создание заказа с разными вариантами цвета")
    def test_create_order_colors_and_track(self, color_fields):
        response = create_order(**color_fields)
        assert response.status_code == HTTPStatus.CREATED
        response_json = response.json()
        assert "track" in response_json
        assert response_json["track"] is not None
