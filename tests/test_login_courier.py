"""Логин курьера: успех, неполный body, неверный логин/пароль, несуществующий пользователь, id в ответе."""

import allure
from http import HTTPStatus

from helpers.api_docs import MSG_ACCOUNT_NOT_FOUND, MSG_LOGIN_INSUFFICIENT
from helpers.courier_helpers import random_string


@allure.feature("Courier")
@allure.story("Логин курьера")
class TestLoginCourier:
    @staticmethod
    def _assert_not_found(response):
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json().get("message") == MSG_ACCOUNT_NOT_FOUND

    @allure.title("Курьер может авторизоваться")
    def test_courier_can_login(self, existing_courier, courier_api_client):
        response = courier_api_client.login(
            existing_courier["login"],
            existing_courier["password"],
        )
        assert response.status_code == HTTPStatus.OK
        response_json = response.json()
        assert "id" in response_json
        assert response_json["id"] == existing_courier["id"]

    @allure.title("Без логина в body (только пароль) - 400")
    def test_login_requires_login_field(self, courier_api_client):
        response = courier_api_client.login_with_body({"password": random_string(10)})
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

    @allure.title("Нет поля login в body - 400")
    def test_missing_login_field_in_body(self, existing_courier, courier_api_client):
        response = courier_api_client.login_with_body(
            {"password": existing_courier["password"]},
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
        response_json = response.json()
        assert "id" in response_json
        assert response_json["id"] == existing_courier["id"]
