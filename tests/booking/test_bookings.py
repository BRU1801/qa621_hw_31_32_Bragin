import json
from pathlib import Path

import pytest
from app.booking import BookingApi, FEATURES

pytestmark = pytest.mark.regression

# Загрузка кейсов из JSON на уровне модуля
CASES_FILE = Path(__file__).parent.parent.parent / "data" / "booking_cases.json"
with open(CASES_FILE, encoding="utf-8") as f:
    BOOKING_CASES = json.load(f)


@pytest.mark.smoke
@pytest.mark.parametrize("room", ["small", "medium", "large"], ids=lambda r: f"room-{r}")
@pytest.mark.parametrize("hours", [1, 4, 8], ids=lambda h: f"hours-{h}")
def test_create_booking_all_rooms_and_hours(user_api, room, hours):
    """Стек параметризации (B3): 3 комнаты × 3 длительности = 9 кейсов."""
    capacity = {"small": 4, "medium": 8, "large": 20}[room]
    response = user_api.create_booking(room, capacity, hours)
    assert response["status"] == 201
    data = response["data"]
    assert data["room"] == room
    assert data["hours"] == hours
    assert data["status"] == "active"


@pytest.mark.parametrize("case", BOOKING_CASES, ids=lambda c: c["id"])
def test_booking_boundary_cases(user_api, case):
    """B4-B6: граничные значения из JSON-файла."""
    response = user_api.create_booking(case["room"], case["people"], case["hours"])
    assert response["status"] == case["expected_status"]


@pytest.mark.parametrize("role", [
    pytest.param("visitor", id="role-visitor"),
    pytest.param("moderator", id="role-moderator"),
    pytest.param("", id="role-empty"),
])
def test_unknown_role_raises_error(role):
    """B7: неизвестная роль вызывает ValueError."""
    with pytest.raises(ValueError, match="Неизвестная роль"):
        BookingApi(role=role)


def test_cancel_booking_success(user_api, booking):
    """B8: успешная отмена."""
    response = user_api.cancel_booking(booking["id"])
    assert response["status"] == 200
    assert response["data"]["status"] == "cancelled"


def test_cancel_booking_already_cancelled(user_api, booking):
    """B8: повторная отмена — 409."""
    user_api.cancel_booking(booking["id"])
    response = user_api.cancel_booking(booking["id"])
    assert response["status"] == 409


def test_cancel_booking_not_found(user_api):
    """B8: отмена несуществующей брони — 404."""
    response = user_api.cancel_booking(9999)
    assert response["status"] == 404


@pytest.mark.skipif(
    not FEATURES["online_payment"],
    reason="Онлайн-оплата выключена (FEATURES['online_payment'] == False)"
)
def test_pay_booking_when_enabled(user_api, booking):
    """B9: оплата при включённом флаге."""
    response = user_api.pay_booking(booking["id"])
    assert response["status"] == 200
    assert response["data"]["status"] == "paid"


@pytest.mark.skipif(
    FEATURES["online_payment"],
    reason="Онлайн-оплата включена (FEATURES['online_payment'] == True)"
)
def test_pay_booking_when_disabled(user_api, booking):
    """B9: оплата при выключенном флаге — 501."""
    response = user_api.pay_booking(booking["id"])
    assert response["status"] == 501