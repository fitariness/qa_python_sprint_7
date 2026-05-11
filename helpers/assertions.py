"""Повторяющиеся проверки ответов API"""


def assert_status(response, expected, msg=""):
    assert response.status_code == expected, (
        msg or f"HTTP {response.status_code}, ожидали {expected}: {response.text[:300]}"
    )


def assert_courier_created(body):
    assert body == {"ok": True}, f"В теле должно быть только ok: true, а пришло: {body!r}"
