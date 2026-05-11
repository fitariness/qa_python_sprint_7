"""Создание заказа: варианты цвета (параметризация), наличие track в ответе."""

import allure
import pytest
from http import HTTPStatus

from helpers.order_helpers import create_order


@allure.feature("Orders")
@allure.story("Создание заказа")
class TestCreateOrder:
    @pytest.mark.parametrize(
        "color_fields",
        [
            pytest.param({"color": ["BLACK"]}, id="black"),
            pytest.param({"color": ["GREY"]}, id="grey"),
            pytest.param({"color": ["BLACK", "GREY"]}, id="both_colors"),
            pytest.param({}, id="no_color"),
        ],
    )
    @allure.title("Создание заказа с разными вариантами цвета")
    def test_create_order_colors_and_track(self, color_fields):
        response = create_order(**color_fields)
        assert response.status_code == HTTPStatus.CREATED
        body = response.json()
        assert "track" in body
        assert body["track"] is not None
