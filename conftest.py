from http import HTTPStatus

import pytest

from helpers.courier_helpers import (
    delete_courier,
    delete_courier_by_credentials,
    random_string,
    register_courier_with_id,
)
from helpers.order_helpers import (
    cancel_order_by_track,
    create_order,
    finish_order,
    get_order_by_track,
)
from pages.courier_api import CourierApi
from pages.orders_api import OrdersApi


def _register_courier_or_fail():
    """Создаёт курьера через API"""
    courier = register_courier_with_id()
    if courier is None:
        pytest.fail("Регистрация курьера не вернула данные")
    return courier


def _create_order_track_or_fail():
    """Создаёт заказ, возвращает track"""
    order_response = create_order()
    if order_response.status_code != HTTPStatus.CREATED:
        pytest.fail(
            f"Ожидался статус {HTTPStatus.CREATED} при создании заказа, "
            f"получен {order_response.status_code}",
        )
    return order_response.json()["track"]


def _order_id_by_track_or_fail(track):
    """Получает id заказа по track"""
    track_response = get_order_by_track(track)
    if track_response.status_code != HTTPStatus.OK:
        pytest.fail(
            f"Ожидался статус {HTTPStatus.OK} при получении заказа по треку, "
            f"получен {track_response.status_code}",
        )
    return track_response.json()["order"]["id"]


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
    courier = _register_courier_or_fail()
    yield courier
    delete_courier(courier["id"])


@pytest.fixture
def courier_and_order():
    """Курьер и заказ в работе; после теста заказ завершается/отменяется, курьер удаляется."""
    courier = _register_courier_or_fail()
    track = _create_order_track_or_fail()
    order_id = _order_id_by_track_or_fail(track)
    context = {
        "courier_id": courier["id"],
        "order_id": order_id,
        "track": track,
    }
    yield context
    finish_response = finish_order(order_id)
    if finish_response.status_code != HTTPStatus.OK:
        cancel_order_by_track(track)
    delete_courier(courier["id"])


@pytest.fixture
def existing_courier():
    """Зарегистрированный курьер (логин, пароль, id); после теста удаляется."""
    data = _register_courier_or_fail()
    yield {"login": data["login"], "password": data["password"], "id": data["id"]}
    delete_courier(data["id"])


@pytest.fixture
def courier_for_delete():
    """Id зарегистрированного курьера; после теста курьер удаляется (если ещё существует)."""
    data = _register_courier_or_fail()
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
    track = _create_order_track_or_fail()
    yield track
    cancel_order_by_track(track)
