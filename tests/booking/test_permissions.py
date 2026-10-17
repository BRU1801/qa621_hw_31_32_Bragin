import pytest
from app.booking import BookingApi

pytestmark = pytest.mark.permissions

# Таблица прав из ТЗ + кейс с багом (только один кейс для guest + list_bookings)
PERMISSIONS_TABLE = [
    pytest.param("guest", "create_booking", 403, id="guest-create_booking"),
    pytest.param("user", "create_booking", 201, id="user-create_booking"),
    pytest.param("admin", "create_booking", 201, id="admin-create_booking"),

    # BUG-1: guest должен получать 403 на list_bookings, но код не проверяет guest
    pytest.param("guest", "list_bookings", 403,
                 marks=pytest.mark.xfail(strict=True,
                                         reason="BUG-1: list_bookings не проверяет роль guest, возвращает 200 вместо 403"),
                 id="guest-list_bookings"),

    pytest.param("user", "list_bookings", 403, id="user-list_bookings"),
    pytest.param("admin", "list_bookings", 200, id="admin-list_bookings"),

    pytest.param("guest", "cancel_booking", 403, id="guest-cancel_booking"),
    pytest.param("user", "cancel_booking", 200, id="user-cancel_booking"),
    pytest.param("admin", "cancel_booking", 200, id="admin-cancel_booking"),

    pytest.param("guest", "pay_booking", 403, id="guest-pay_booking"),
    pytest.param("user", "pay_booking", 501, id="user-pay_booking-disabled"),
    pytest.param("admin", "pay_booking", 501, id="admin-pay_booking-disabled"),
]

ACTIONS = {
    "create_booking": lambda api: api.create_booking("small", 2, 1),
    "list_bookings": lambda api: api.list_bookings(),
    "cancel_booking": lambda api: api.cancel_booking(1),
    "pay_booking": lambda api: api.pay_booking(1),
}


@pytest.mark.parametrize("role,action,expected_status", PERMISSIONS_TABLE)
def test_permissions_matrix(role, action, expected_status):
    """Проверка матрицы прав доступа."""
    api = BookingApi(role=role)

    # Для cancel и pay нужна существующая бронь.
    # Создаём её через user_api и подменяем хранилище, чтобы api её видел.
    if action in ("cancel_booking", "pay_booking"):
        user_api = BookingApi(role="user")
        user_api.create_booking("small", 2, 1)
        api._bookings = user_api._bookings
        api._next_id = user_api._next_id

    response = ACTIONS[action](api)
    assert response["status"] == expected_status