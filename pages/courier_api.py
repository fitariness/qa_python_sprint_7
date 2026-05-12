import allure
import requests

from pages.base_api import BaseApi
from pages.locators import ScooterUrls


class CourierApi(BaseApi):
    """Page Object для ручек курьера"""

    @allure.step("Создание курьера")
    def create_courier(self, login, password, first_name):
        return requests.post(
            self._url(ScooterUrls.COURIER),
            json={"login": login, "password": password, "firstName": first_name},
            timeout=self.timeout,
        )

    @allure.step("POST /courier с произвольным body JSON")
    def post_courier_body(self, body):
        """POST на тот же URL, что и у create_courier (`ScooterUrls.COURIER`), но JSON собираем сами

        Нужен для негативных и краевых кейсов; успешное создание - через create_courier
        """
        return requests.post(
            self._url(ScooterUrls.COURIER),
            json=body,
            timeout=self.timeout,
        )

    @allure.step("Логин курьера")
    def login(self, login, password):
        return requests.post(
            self._url(ScooterUrls.COURIER_LOGIN),
            json={"login": login, "password": password},
            timeout=self.timeout,
        )

    @allure.step("Логин курьера с произвольным body JSON")
    def login_with_body(self, body):
        """POST на тот же URL, что и у login, но body запроса собираем сами (негативные сценарии)"""
        return requests.post(
            self._url(ScooterUrls.COURIER_LOGIN),
            json=body,
            timeout=self.timeout,
        )

    @allure.step("Удаление курьера по id")
    def delete(self, courier_id):
        return requests.delete(
            self._url(ScooterUrls.courier_by_id(courier_id)),
            timeout=self.timeout,
        )

    @allure.step("DELETE /courier без id в пути")
    def delete_without_courier_id(self):
        """DELETE /api/v1/courier без id в пути"""
        return requests.delete(
            self._url(ScooterUrls.COURIER),
            timeout=self.timeout,
        )
