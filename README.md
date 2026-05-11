# Автотесты API «Яндекс Самокат» (qa-scooter)

Тесты на **pytest** и **requests** к стенду `https://qa-scooter.praktikum-services.ru`
Отчёты собираются через **Allure**

Базовый адрес стенда задаётся один раз в **`pages/locators.py`** (`ScooterUrls.BASE`). Остальные пути к эндпоинтам - там же.

### Основная часть

- `tests/test_create_courier.py` - создание курьера
- `tests/test_login_courier.py` - логин курьера
- `tests/test_create_order.py` - создание заказа (в т.ч. параметризация по цвету)
- `tests/test_orders_list.py` - список заказов
- отчёт **Allure**

### Дополнительное задание (три ручки)

- `tests/test_delete_courier.py` - удаление курьера
- `tests/test_accept_order.py` - принятие заказа
- `tests/test_get_order_by_track.py` - заказ по номеру (треку)

## Установка зависимостей проекта

```bash
python3 -m venv .venv
pip install -r requirements.txt
```

## Как запустить тесты

Все тесты:

```bash
pytest
```

Один модуль или один тест:

```bash
pytest tests/test_create_courier.py -v
pytest tests/test_login_courier.py::TestLoginCourier::test_courier_can_login -v
```

## Отчёт Allure

После генерации запускать локальный сервер командой **`allure open`**:

1. Результаты прогона:

   ```bash
   pytest tests/ --alluredir=allure_results
   ```

2. Сборка HTML:

   ```bash
   allure generate allure_results -o allure_report --clean
   ```

3. **Открытие в браузере по HTTP**:

   ```bash
   allure open allure_report
   ```
