import pytest

from pages.courier_api import CourierApi
from pages.orders_api import OrdersApi


@pytest.fixture
def courier_api_client():
    """Клиент API курьера (Page Object)"""
    return CourierApi()


@pytest.fixture
def orders_api_client():
    """Клиент API заказов (Page Object)"""
    return OrdersApi()
