"""
URL API: базовый адрес стенда и относительные пути.
"""


class ScooterUrls:
    BASE = "https://qa-scooter.praktikum-services.ru"
    API_V1 = "/api/v1"

    COURIER = f"{API_V1}/courier"
    COURIER_LOGIN = f"{API_V1}/courier/login"
    ORDERS = f"{API_V1}/orders"
    ORDERS_TRACK = f"{API_V1}/orders/track"
    ORDERS_CANCEL = f"{API_V1}/orders/cancel"
    ORDERS_ACCEPT_ROOT = f"{API_V1}/orders/accept/"

    @classmethod
    def courier_by_id(cls, courier_id):
        return f"{cls.COURIER}/{courier_id}"

    @classmethod
    def orders_accept(cls, order_id):
        return f"{cls.ORDERS}/accept/{order_id}"

    @classmethod
    def orders_finish(cls, order_id):
        return f"{cls.ORDERS}/finish/{order_id}"
