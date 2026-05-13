from http import HTTPStatus

from helpers.courier_helpers import random_string
from pages.orders_api import OrdersApi
from testdata.orders import DEFAULT_ORDER_BASE

_default_orders_api = OrdersApi()


def orders_api():
    return _default_orders_api


def sample_order_body(**overrides):
    """Сборка body заказа: базовые поля из testdata + уникальный comment"""
    body = {**DEFAULT_ORDER_BASE, "comment": random_string(8)}
    body.update(overrides)
    return body


def create_order(**overrides):
    return orders_api().create(sample_order_body(**overrides))


def get_order_by_track(track):
    return orders_api().track(track)


def cancel_order_by_track(track):
    return orders_api().cancel_by_track(track)


def accept_order(order_id, courier_id):
    return orders_api().accept(order_id=order_id, courier_id=courier_id)


def finish_order(order_id):
    return orders_api().finish(order_id)


def create_order_track_or_raise():
    """Создаём заказ и возвращаем track, при неожиданном статусе - RuntimeError"""
    order_response = create_order()
    if order_response.status_code != HTTPStatus.CREATED:
        raise RuntimeError(
            f"Создание заказа: ожидался HTTP {HTTPStatus.CREATED}, "
            f"получен {order_response.status_code}",
        )
    return order_response.json()["track"]


def order_id_by_track_or_raise(track):
    """У заказа по track получаем числовой id, при неожиданном статусе - RuntimeError"""
    track_response = get_order_by_track(track)
    if track_response.status_code != HTTPStatus.OK:
        raise RuntimeError(
            f"Заказ по track: ожидался HTTP {HTTPStatus.OK}, "
            f"получен {track_response.status_code}",
        )
    return track_response.json()["order"]["id"]


def finish_order_or_cancel_by_track(order_id, track):
    """Завершение заказа, если не вышло - отменяем по track (очистка после теста)"""
    finish_response = finish_order(order_id)
    if finish_response.status_code != HTTPStatus.OK:
        cancel_order_by_track(track)
