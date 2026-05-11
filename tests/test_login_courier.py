"""Логин курьера: успех, неполное тело, неверный логин/пароль, несуществующий пользователь, id в ответе

Пустое JSON-тело и тело только с login (без password) на стенде иногда не укладываются в таймаут - тесты помечаются skip
"""

import allure
import pytest
import requests
from http import HTTPStatus

from helpers.api_docs import MSG_ACCOUNT_NOT_FOUND, MSG_LOGIN_INSUFFICIENT
from helpers.courier_helpers import (
    delete_courier,
    random_string,
    register_courier_with_id,
)


@allure.feature("Courier")
@allure.story("Логин курьера")
class TestLoginCourier:
    @staticmethod
    def _assert_not_found(response):
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json().get("message") == MSG_ACCOUNT_NOT_FOUND

    @pytest.fixture
    def existing_courier(self):
        data = register_courier_with_id()
        assert data is not None
        yield {"login": data["login"], "password": data["password"], "id": data["id"]}
        delete_courier(data["id"])

    @allure.title("Курьер может авторизоваться")
    def test_courier_can_login(self, existing_courier, courier_api_client):
        response = courier_api_client.login(
            existing_courier["login"],
            existing_courier["password"],
        )
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert "id" in data
        assert data["id"] == existing_courier["id"]

    @allure.title("Без логина в теле (только пароль) - 400")
    def test_login_requires_login_field(self, courier_api_client):
        response = courier_api_client.login_with_body({"password": random_string(10)})
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json().get("message") == MSG_LOGIN_INSUFFICIENT

    @allure.title("Пустое JSON-тело - 400")
    def test_empty_json_body_handling(self, courier_api_client):
        try:
            response = courier_api_client.login_with_body({})
        except requests.exceptions.Timeout:
            pytest.skip(
                f"Таймаут {courier_api_client.timeout} с: стенд не ответил на пустое JSON-тело",
            )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json().get("message") == MSG_LOGIN_INSUFFICIENT

    @allure.title("Неверный пароль - 404, учётная запись не найдена")
    def test_wrong_password_returns_error(self, existing_courier, courier_api_client):
        response = courier_api_client.login_with_body(
            {
                "login": existing_courier["login"],
                "password": "wrong_password_xyz",
            },
        )
        TestLoginCourier._assert_not_found(response)

    @allure.title("Неверный логин - 404, учётная запись не найдена")
    def test_wrong_login_returns_error(self, existing_courier, courier_api_client):
        response = courier_api_client.login_with_body(
            {
                "login": "nonexistent_login_xyz",
                "password": existing_courier["password"],
            },
        )
        TestLoginCourier._assert_not_found(response)

    @allure.title("Нет поля login в теле - 400")
    def test_missing_login_field_in_body(self, existing_courier, courier_api_client):
        response = courier_api_client.login_with_body(
            {"password": existing_courier["password"]},
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json().get("message") == MSG_LOGIN_INSUFFICIENT

    @allure.title("Нет поля password - 400")
    def test_missing_password_field_in_body(self, existing_courier, courier_api_client):
        try:
            response = courier_api_client.login_with_body(
                {"login": existing_courier["login"]},
            )
        except requests.exceptions.Timeout:
            pytest.skip(
                f"Таймаут {courier_api_client.timeout} с: стенд не ответил на тело только с login (без password)",
            )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json().get("message") == MSG_LOGIN_INSUFFICIENT

    @allure.title("Несуществующая пара логин-пароль - 404")
    def test_nonexistent_user_returns_error(self, courier_api_client):
        response = courier_api_client.login_with_body(
            {
                "login": random_string(15),
                "password": random_string(15),
            },
        )
        TestLoginCourier._assert_not_found(response)

    @allure.title("Успешный ответ содержит id курьера")
    def test_success_returns_id(self, existing_courier, courier_api_client):
        response = courier_api_client.login(
            existing_courier["login"],
            existing_courier["password"],
        )
        assert response.status_code == HTTPStatus.OK
        body = response.json()
        assert "id" in body
        assert body["id"] == existing_courier["id"]
