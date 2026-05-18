"""Тексты ответов API из документации Swagger"""

MSG_LOGIN_INSUFFICIENT = "Недостаточно данных для входа"
MSG_ACCOUNT_NOT_FOUND = "Учетная запись не найдена"
MSG_COURIER_CREATE_INSUFFICIENT = "Недостаточно данных для создания учетной записи"
MSG_COURIER_LOGIN_TAKEN = "Этот логин уже используется. Попробуйте другой."
# Фактический ответ стенда
MSG_COURIER_NOT_FOUND_BY_ID = "Курьера с таким id нет."
MSG_DELETE_NO_ID_NOT_FOUND = "Not Found."
MSG_SEARCH_INSUFFICIENT = "Недостаточно данных для поиска"

# Заказы / принятие / завершение / трек
MSG_ORDER_NOT_FOUND = "Заказ не найден"
MSG_ACCEPT_ORDER_ID_NOT_EXISTS = "Заказа с таким id не существует"
MSG_ACCEPT_COURIER_ID_NOT_EXISTS = "Курьера с таким id не существует"
MSG_HTTP_NOT_FOUND_DOT = "Not Found."


def courier_not_found_message(courier_id):
    """Текст ошибки, когда в списке заказов ищут по несуществующему курьеру"""
    return f"Курьер с идентификатором {courier_id} не найден"
