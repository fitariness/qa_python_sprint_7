"""Повторяющиеся проверки ответов API"""


def assert_status(response, expected, msg=""):
    assert response.status_code == expected, (
        msg or f"HTTP {response.status_code}, ожидали {expected}: {response.text[:300]}"
    )


def assert_courier_created(response_json):
    assert response_json == {
        "ok": True
    }, f"В JSON ответе ожидалось {{'ok': True}}, пришло: {response_json!r}"
