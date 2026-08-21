class Reservation:
    def __init__(self, reservation_id, passenger_id, flight_number, seat_number, price, status="Confirmed"):
        self.reservation_id = reservation_id
        self.passenger_id = passenger_id
        self.flight_number = flight_number
        self.seat_number = seat_number
        self.price = price
        self.status = status

    def cancel(self):
        self.status = "Cancelled"

    def to_dict(self):
        return {
            "reservation_id": self.reservation_id,
            "passenger_id": self.passenger_id,
            "flight_number": self.flight_number,
            "seat_number": self.seat_number,
            "price": self.price,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["reservation_id"], data["passenger_id"], data["flight_number"],
            data["seat_number"], data["price"], data["status"]
        )