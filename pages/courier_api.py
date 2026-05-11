import requests

from pages.base_api import BaseApi
from pages.locators import ScooterUrls


class CourierApi(BaseApi):
    """Page Object для ручек курьера"""

    def create_courier(self, login, password, first_name):
        return requests.post(
            self._url(ScooterUrls.COURIER),
            json={"login": login, "password": password, "firstName": first_name},
            timeout=self.timeout,
        )

    def post_courier_body(self, body):
        """POST на тот же URL, что и у create_courier (`ScooterUrls.COURIER`), но JSON собираем сами

        Нужен для негативных и краевых кейсов; успешное создание - через create_courier
        """
        return requests.post(
            self._url(ScooterUrls.COURIER),
            json=body,
            timeout=self.timeout,
        )

    def login(self, login, password):
        return requests.post(
            self._url(ScooterUrls.COURIER_LOGIN),
            json={"login": login, "password": password},
            timeout=self.timeout,
        )

    def login_with_body(self, body):
        """POST на тот же URL, что и у login, но тело запроса собираем сами (негативные сценарии)"""
        return requests.post(
            self._url(ScooterUrls.COURIER_LOGIN),
            json=body,
            timeout=self.timeout,
        )

    def delete(self, courier_id):
        return requests.delete(
            self._url(ScooterUrls.courier_by_id(courier_id)),
            timeout=self.timeout,
        )

    def delete_without_courier_id(self):
        """DELETE /api/v1/courier без id в пути"""
        return requests.delete(
            self._url(ScooterUrls.COURIER),
            timeout=self.timeout,
        )
