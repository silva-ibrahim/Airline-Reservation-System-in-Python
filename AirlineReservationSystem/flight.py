class Flight:
    def __init__(self, flight_number, departure, destination, date, time, aircraft, price):
        self.flight_number = flight_number
        self.departure = departure
        self.destination = destination
        self.date = date
        self.time = time
        self.aircraft = aircraft
        self.price = price
        self.status = "Scheduled"

        self.seats = self._create_seats()

    def _create_seats(self):
        seats = {}
        columns = ["A", "B", "C", "D", "E", "F"]

        for row in range(1, 11):
            for column in columns:
                seat_number = f"{row}{column}"
                seats[seat_number] = "Available"
        return seats

    def reserve_seat(self, seat_number):
        if seat_number not in self.seats:
            return False, "This seat does not exist."

        if self.seats[seat_number] == "Occupied":
            return False, "This seat is already reserved."
        self.seats[seat_number] = "Occupied"
        return True, "Seat reserved successfully."

    def release_seat(self, seat_number):
        if seat_number not in self.seats:
            return False

        self.seats[seat_number] = "Available"
        return True

    def available_seat_count(self):
        return sum(1 for status in self.seats.values() if status == "Available")

    def to_dict(self):
        return {
            "flight_number": self.flight_number,
            "departure": self.departure,
            "destination": self.destination,
            "date": self.date,
            "time": self.time,
            "aircraft": self.aircraft,
            "price": self.price,
            "status": self.status,
            "seats": self.seats
        }

    @classmethod
    def from_dict(cls, data):
        flight = cls(
            data["flight_number"], data["departure"], data["destination"],
            data["date"], data["time"], data["aircraft"], data["price"]
        )

        flight.status = data["status"]
        flight.seats = data["seats"]

        return flight