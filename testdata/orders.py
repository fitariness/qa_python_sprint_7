"""Тестовые данные для ручек заказов (как в документации учебного сервиса)."""

import pytest

DEFAULT_ORDER_BASE = {
    "firstName": "Naruto",
    "lastName": "Uchiha",
    "address": "Konoha, 142 apt.",
    "metroStation": "4",
    "phone": "+7 800 355 35 35",
    "rentTime": 5,
    "deliveryDate": "2026-06-06",
}

CREATE_ORDER_COLOR_PARAMS = [
    pytest.param({"color": ["BLACK"]}, id="black"),
    pytest.param({"color": ["GREY"]}, id="grey"),
    pytest.param({"color": ["BLACK", "GREY"]}, id="both_colors"),
    pytest.param({"color": []}, id="no_color"),
]
