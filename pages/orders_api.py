import requests

from pages.base_api import BaseApi
from pages.locators import ScooterUrls


class OrdersApi(BaseApi):
    """Page Object для ручек заказов"""

    def create(self, payload):
        return requests.post(
            self._url(ScooterUrls.ORDERS),
            json=payload,
            timeout=self.timeout,
        )

    def track(self, track=None):
        params = {"t": track} if track is not None else None
        return requests.get(
            self._url(ScooterUrls.ORDERS_TRACK),
            params=params,
            timeout=self.timeout,
        )

    def cancel_by_track(self, track):
        return requests.put(
            self._url(ScooterUrls.ORDERS_CANCEL),
            params={"track": track},
            timeout=self.timeout,
        )

    def accept(self, order_id=None, courier_id=None):
        if order_id is None:
            url = self._url(ScooterUrls.ORDERS_ACCEPT_ROOT)
        else:
            url = self._url(ScooterUrls.orders_accept(order_id))
        kwargs = {"timeout": self.timeout}
        if courier_id is not None:
            kwargs["params"] = {"courierId": courier_id}
        return requests.put(url, **kwargs)

    def finish(self, order_id):
        """По заданию id передаётся в query (?id=...)"""
        return requests.put(
            self._url(ScooterUrls.orders_finish(order_id)),
            params={"id": order_id},
            timeout=self.timeout,
        )

    def list_orders(self, **params):
        return requests.get(
            self._url(ScooterUrls.ORDERS),
            params=params or None,
            timeout=self.timeout,
        )
