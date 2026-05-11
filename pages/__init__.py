"""Слой Page Object для REST API (эндпоинты + клиенты)"""

from pages.courier_api import CourierApi
from pages.orders_api import OrdersApi

__all__ = ["CourierApi", "OrdersApi"]
