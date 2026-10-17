import pytest
from app.booking import BookingApi

pytestmark = pytest.mark.smoke


def test_health(any_api):
    """B1: health() всегда возвращает 200."""
    response = any_api.health()
    assert response["status"] == 200
    assert response["data"]["service"] == "booking"
    assert response["data"]["ok"] is True


def test_list_rooms(any_api):
    """B2: list_rooms() возвращает 200 и список из трёх переговорок."""
    response = any_api.list_rooms()
    assert response["status"] == 200
    rooms = response["data"]
    assert len(rooms) == 3
    names = [r["name"] for r in rooms]
    assert "small" in names
    assert "medium" in names
    assert "large" in names


@pytest.mark.parametrize("room,people,hours", [
    pytest.param("small", 2, 1, id="small-2-1"),
    pytest.param("medium", 4, 2, id="medium-4-2"),
    pytest.param("large", 10, 4, id="large-10-4"),
])
def test_create_booking_success(user_api, room, people, hours):
    """B3: успешное создание брони."""
    response = user_api.create_booking(room, people, hours)
    assert response["status"] == 201
    data = response["data"]
    assert data["room"] == room
    assert data["people"] == people
    assert data["hours"] == hours
    assert data["status"] == "active"
    assert "id" in data