import pytest
from app.booking import BookingApi


@pytest.fixture(params=["guest", "user", "admin"], ids=lambda r: f"role-{r}")
def any_api(request):
    """Клиент API с каждой из трёх ролей."""
    return BookingApi(role=request.param)


@pytest.fixture
def user_api():
    """Клиент API с ролью user."""
    return BookingApi(role="user")


@pytest.fixture
def booking(user_api):
    """Создаёт бронь, отдаёт тесту, после теста отменяет."""
    response = user_api.create_booking("small", 2, 1)
    yield response["data"]
    user_api.cancel_booking(response["data"]["id"])


def pytest_html_report_title(report):
    report.title = "QA621 ДЗ 31-32: Брагин"