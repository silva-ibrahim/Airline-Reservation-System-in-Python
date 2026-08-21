from passenger import Passenger
from flight import Flight
from reservation import Reservation


class AirlineManager:

    def __init__(self):
        self.passengers = []
        self.flights = []
        self.reservations = []

    def add_passenger(self, name, surname, email, phone, passport_number):
        passenger_id = self._generate_passenger_id()
        passenger = Passenger(passenger_id, name, surname, email, phone, passport_number)
        self.passengers.append(passenger)
        return passenger

    def find_passenger(self, passenger_id):
        passenger_id = passenger_id.strip().upper()

        for passenger in self.passengers:
            if passenger.passenger_id.upper() == passenger_id:
                return passenger
        return None

    def add_flight(self, flight_number, departure, destination, date, time, aircraft, price):        
        if self.find_flight(flight_number):
            return None

        flight = Flight(flight_number, departure, destination, date, time, aircraft, price)
        self.flights.append(flight)

        return flight

    def find_flight(self, flight_number):
        flight_number = flight_number.strip().upper()

        for flight in self.flights:
            if flight.flight_number.upper() == flight_number:
                return flight
        return None

    def search_flights(self, departure, destination, date):
        results = []

        for flight in self.flights:
            if (
                flight.departure.lower() == departure.lower() and
                flight.destination.lower() == destination.lower() and
                flight.date == date and
                flight.status == "Scheduled"):
                results.append(flight)
        return results

    def create_reservation(self, passenger_id, flight_number, seat_number):
        passenger = self.find_passenger(passenger_id)

        if passenger is None:
            return None, "Passenger not found."

        flight = self.find_flight(flight_number)

        if flight is None:
            return None, "Flight not found."

        for reservation in self.reservations:
            if (reservation.passenger_id.upper() == passenger_id.strip().upper() and
                reservation.flight_number.upper() == flight_number.strip().upper() and
                reservation.status == "Confirmed"):
                return None, "This passenger already has an active reservation for this flight."

        seat_number = seat_number.strip().upper()

        success, message = flight.reserve_seat(seat_number)

        if not success:
            return None, message

        reservation_id = self._generate_reservation_id()
        reservation = Reservation(reservation_id, passenger_id, flight_number, seat_number, flight.price)
        self.reservations.append(reservation)

        return reservation, "Reservation created successfully."

    def find_reservation(self, reservation_id):
        reservation_id = reservation_id.strip().upper()

        if reservation_id.isdigit():
            reservation_id = f"RES-{int(reservation_id):04d}"

        for reservation in self.reservations:
            if (reservation.reservation_id.upper() == reservation_id):
                return reservation
        return None

    def cancel_reservation(self, reservation_id):
        reservation = self.find_reservation(reservation_id)

        if reservation is None:
            return False, "Reservation not found."

        if reservation.status == "Cancelled":
            return False, "This reservation has already been cancelled."

        flight = self.find_flight(reservation.flight_number)

        if flight:
            flight.release_seat(reservation.seat_number)
        reservation.cancel()
        return True, "Reservation cancelled successfully."

    def total_revenue(self):
        return sum(reservation.price for reservation in self.reservations if reservation.status == "Confirmed")

    def total_confirmed_reservations(self):
        return sum(1 for reservation in self.reservations if reservation.status == "Confirmed")

    def _generate_passenger_id(self):
        return f"P{len(self.passengers) + 1:04d}"

    def _generate_reservation_id(self):
        return f"RES-{len(self.reservations) + 1:04d}"