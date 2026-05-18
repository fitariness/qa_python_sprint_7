import pytest

from helpers.courier_helpers import (
    delete_courier,
    delete_courier_by_credentials,
    random_string,
    register_courier_with_id_or_raise,
)
from helpers.order_helpers import (
    cancel_order_by_track,
    create_order_track_or_raise,
    finish_order_or_cancel_by_track,
    order_id_by_track_or_raise,
)
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


@pytest.fixture
def courier_only():
    """Курьер без заказа; после теста удаляется."""
    courier = register_courier_with_id_or_raise()
    yield courier
    delete_courier(courier["id"])


@pytest.fixture
def courier_and_order():
    """Курьер и заказ в работе; после теста заказ завершается/отменяется, курьер удаляется."""
    courier = register_courier_with_id_or_raise()
    track = create_order_track_or_raise()
    order_id = order_id_by_track_or_raise(track)
    context = {
        "courier_id": courier["id"],
        "order_id": order_id,
        "track": track,
    }
    yield context
    finish_order_or_cancel_by_track(order_id, track)
    delete_courier(courier["id"])


@pytest.fixture
def existing_courier():
    """Зарегистрированный курьер (логин, пароль, id); после теста удаляется."""
    data = register_courier_with_id_or_raise()
    yield {"login": data["login"], "password": data["password"], "id": data["id"]}
    delete_courier(data["id"])


@pytest.fixture
def courier_for_delete():
    """Id зарегистрированного курьера; после теста курьер удаляется"""
    data = register_courier_with_id_or_raise()
    courier_id = data["id"]
    yield courier_id
    delete_courier(courier_id)


@pytest.fixture
def random_courier_credentials():
    """Рандомные логин, пароль и имя для сценариев создания курьера"""
    return random_string(10), random_string(10), random_string(10)


@pytest.fixture
def cleanup_registered_courier_credentials():
    """Список пар (login, password): тест регистрирует курьера, добавляет пару - после теста удаление"""
    pairs = []
    yield pairs
    for login, password in pairs:
        delete_courier_by_credentials(login, password)


@pytest.fixture
def created_order_track():
    """Заказ с track, после теста отмена по track"""
    track = create_order_track_or_raise()
    yield track
    cancel_order_by_track(track)
