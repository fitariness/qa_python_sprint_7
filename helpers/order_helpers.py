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
