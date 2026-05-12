from http import HTTPStatus
import random
import string

from pages.courier_api import CourierApi

_shared_courier_client = CourierApi()


def random_string(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length))


def courier_api():
    """Общий клиент курьера для хелперов"""
    return _shared_courier_client


def register_random_courier():
    """Случайные логин, пароль и имя (POST /api/v1/courier)

    Если ответ HTTP 201 Created, вернётся список из трёх строк: логин, пароль, имя
    Иначе - пустой список
    """
    result = []
    login = random_string(10)
    password = random_string(10)
    first_name = random_string(10)
    api = courier_api()
    response = api.create_courier(login, password, first_name)
    if response.status_code == HTTPStatus.CREATED:
        result.extend([login, password, first_name])
    return result


def register_courier_with_id():
    """Создаёт курьера, логинится и возвращает словарь с id или None, если что-то пошло не так"""
    creds = register_random_courier()
    if len(creds) != 3:
        return None
    login, password, first_name = creds
    api = courier_api()
    login_response = api.login(login, password)
    if login_response.status_code != HTTPStatus.OK:
        return None
    courier_id = login_response.json().get("id")
    if courier_id is None:
        return None
    return {
        "login": login,
        "password": password,
        "first_name": first_name,
        "id": courier_id,
    }


def delete_courier(courier_id):
    return courier_api().delete(courier_id)


def login_courier(login, password):
    return courier_api().login(login, password)


def delete_courier_by_credentials(login, password):
    """Удаляет курьера после успешного логина"""
    login_response = login_courier(login, password)
    if login_response.status_code != HTTPStatus.OK:
        return
    courier_id = login_response.json().get("id")
    if courier_id is not None:
        delete_courier(courier_id)
