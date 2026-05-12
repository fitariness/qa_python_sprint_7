"""Удаление курьера: успех, запрос без id, несуществующий id, сообщение об ошибке."""

import allure
from http import HTTPStatus

from helpers.api_docs import MSG_COURIER_NOT_FOUND_BY_ID, MSG_DELETE_NO_ID_NOT_FOUND


@allure.feature("Courier")
@allure.story("Удаление курьера")
class TestDeleteCourier:
    @staticmethod
    def _assert_unknown_courier_id(response):
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json().get("message") == MSG_COURIER_NOT_FOUND_BY_ID

    @allure.title("Успешное удаление: 200 и ok: true")
    def test_success_returns_ok_true(self, courier_for_delete, courier_api_client):
        courier_id = courier_for_delete
        response = courier_api_client.delete(courier_id)
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {"ok": True}

    @allure.title("Без id в пути - 404 (на стенде текст Not Found.)")
    def test_delete_without_id_returns_error(self, courier_api_client):
        response = courier_api_client.delete_without_courier_id()
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json().get("message") == MSG_DELETE_NO_ID_NOT_FOUND

    @allure.title("Несуществующий id - 404 и сообщение об ошибке")
    def test_delete_nonexistent_id_returns_error(self, courier_api_client):
        fake_id = 999_999_999
        response = courier_api_client.delete(fake_id)
        self._assert_unknown_courier_id(response)

    @allure.title("Неуспешное удаление: в JSON ответе - сообщение об ошибке")
    def test_unsuccessful_returns_error_message(self, courier_api_client):
        response = courier_api_client.delete(999_999_998)
        self._assert_unknown_courier_id(response)
