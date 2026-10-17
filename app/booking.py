ROOMS = {"small": 4, "medium": 8, "large": 20}
ROLES = ("guest", "user", "admin")
FEATURES = {"online_payment": False}


class BookingApi:
    """Имитация API сервиса бронирования переговорок."""

    def __init__(self, role="user"):
        if role not in ROLES:
            raise ValueError(f"Неизвестная роль: {role}")
        self.role = role
        self._bookings = {}
        self._next_id = 1

    def health(self):
        return {"status": 200, "data": {"service": "booking", "ok": True}}

    def list_rooms(self):
        rooms = [{"name": name, "capacity": capacity}
                 for name, capacity in ROOMS.items()]
        return {"status": 200, "data": rooms}

    def create_booking(self, room, people, hours):
        if self.role == "guest":
            return {"status": 403, "error": "Forbidden"}
        if room not in ROOMS:
            return {"status": 404, "error": "Room not found"}
        if not 1 <= people <= ROOMS[room]:
            return {"status": 400, "error": "Wrong number of people"}
        if not 1 <= hours <= 8:
            return {"status": 400, "error": "Wrong number of hours"}
        booking = {
            "id": self._next_id,
            "room": room,
            "people": people,
            "hours": hours,
            "status": "active",
        }
        self._bookings[self._next_id] = booking
        self._next_id += 1
        return {"status": 201, "data": dict(booking)}

    def get_booking(self, booking_id):
        booking = self._bookings.get(booking_id)
        if booking is None:
            return {"status": 404, "error": "Booking not found"}
        return {"status": 200, "data": dict(booking)}

    def list_bookings(self):
        if self.role == "user":
            return {"status": 403, "error": "Forbidden"}
        return {"status": 200, "data": [dict(b) for b in self._bookings.values()]}

    def cancel_booking(self, booking_id):
        if self.role == "guest":
            return {"status": 403, "error": "Forbidden"}
        booking = self._bookings.get(booking_id)
        if booking is None:
            return {"status": 404, "error": "Booking not found"}
        if booking["status"] == "cancelled":
            return {"status": 409, "error": "Booking already cancelled"}
        booking["status"] = "cancelled"
        return {"status": 200, "data": dict(booking)}

    def pay_booking(self, booking_id):
        if self.role == "guest":
            return {"status": 403, "error": "Forbidden"}
        if not FEATURES["online_payment"]:
            return {"status": 501, "error": "Online payment is disabled"}
        booking = self._bookings.get(booking_id)
        if booking is None:
            return {"status": 404, "error": "Booking not found"}
        if booking["status"] != "active":
            return {"status": 409, "error": "Only active booking can be paid"}
        booking["status"] = "paid"
        return {"status": 200, "data": dict(booking)}