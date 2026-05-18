"""Создание курьера: успех, дубликаты, обязательные поля, коды HTTP и JSON ответа, ошибки."""

import allure
import pytest
from http import HTTPStatus

from helpers.api_docs import MSG_COURIER_CREATE_INSUFFICIENT, MSG_COURIER_LOGIN_TAKEN
from helpers.assertions import assert_courier_created, assert_status
from helpers.courier_helpers import random_string


@allure.feature("Courier")
@allure.story("Создание курьера")
class TestCreateCourier:
    @allure.title("Успешное создание курьера")
    def test_courier_can_be_created(
        self,
        courier_api_client,
        cleanup_registered_courier_credentials,
        random_courier_credentials,
    ):
        login, password, first_name = random_courier_credentials
        response = courier_api_client.create_courier(login, password, first_name)
        cleanup_registered_courier_credentials.append((login, password))
        assert_status(response, HTTPStatus.CREATED)
        assert_courier_created(response.json())

    @allure.title("Два одинаковых курьера создать нельзя")
    def test_cannot_create_duplicate_courier(
        self,
        courier_api_client,
        cleanup_registered_courier_credentials,
        random_courier_credentials,
    ):
        login, password, first_name = random_courier_credentials
        body = {"login": login, "password": password, "firstName": first_name}
        first_response = courier_api_client.post_courier_body(body)
        assert first_response.status_code == HTTPStatus.CREATED
        cleanup_registered_courier_credentials.append((login, password))
        second_response = courier_api_client.post_courier_body(body)
        assert second_response.status_code == HTTPStatus.CONFLICT
        assert second_response.json().get("message") == MSG_COURIER_LOGIN_TAKEN

    @pytest.mark.parametrize(
        "missing_key",
        ["login", "password"],
    )
    @allure.title("Без логина или без пароля сервер отвечает 400")
    def test_login_and_password_required(self, courier_api_client, missing_key):
        body = {
            "login": random_string(10),
            "password": random_string(10),
            "firstName": random_string(10),
        }
        del body[missing_key]
        response = courier_api_client.post_courier_body(body)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json().get("message") == MSG_COURIER_CREATE_INSUFFICIENT

    @allure.title("Без имени: на стенде всё равно 201 (расходится со Swagger)")
    def test_without_first_name_current_api_behavior(
        self,
        courier_api_client,
        cleanup_registered_courier_credentials,
        random_courier_credentials,
    ):
        login, password, _first_name = random_courier_credentials
        response = courier_api_client.post_courier_body(
            {"login": login, "password": password},
        )
        cleanup_registered_courier_credentials.append((login, password))
        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {"ok": True}

    @allure.title("Пустой body - ошибка недостаточно данных")
    def test_empty_body_returns_error(self, courier_api_client):
        response = courier_api_client.post_courier_body({})
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json().get("message") == MSG_COURIER_CREATE_INSUFFICIENT

    @allure.title("При успехе приходит 201 и ok: true")
    def test_success_returns_201_and_ok_true(
        self,
        courier_api_client,
        cleanup_registered_courier_credentials,
        random_courier_credentials,
    ):
        login, password, first_name = random_courier_credentials
        response = courier_api_client.create_courier(login, password, first_name)
        cleanup_registered_courier_credentials.append((login, password))
        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {"ok": True}

    @allure.title("Тот же логин и другой пароль - занято")
    def test_duplicate_login_returns_error(
        self,
        courier_api_client,
        cleanup_registered_courier_credentials,
        random_courier_credentials,
    ):
        login, password_first, name_first = random_courier_credentials
        password_other = random_string(10)
        name_other = random_string(10)
        first_response = courier_api_client.post_courier_body(
            {"login": login, "password": password_first, "firstName": name_first},
        )
        assert first_response.status_code == HTTPStatus.CREATED
        cleanup_registered_courier_credentials.append((login, password_first))
        second_response = courier_api_client.post_courier_body(
            {"login": login, "password": password_other, "firstName": name_other},
        )
        assert second_response.status_code == HTTPStatus.CONFLICT
        assert second_response.json().get("message") == MSG_COURIER_LOGIN_TAKEN
