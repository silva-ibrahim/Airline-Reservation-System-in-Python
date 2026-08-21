import json
import os

from passenger import Passenger
from flight import Flight
from reservation import Reservation


class Storage:

    def __init__(self, passenger_file = "passengers.json", flight_file = "flights.json", reservation_file = "reservations.json"):
        self.passenger_file = passenger_file
        self.flight_file = flight_file
        self.reservation_file = reservation_file

    def save(self, manager):
        with open(self.passenger_file, "w", encoding="utf-8") as f:
            data = [p.to_dict() for p in manager.passengers]
            json.dump(data, f, indent=4, ensure_ascii=False)

        with open(self.flight_file, "w", encoding="utf-8") as f:
            data = [fl.to_dict() for fl in manager.flights]
            json.dump(data, f, indent=4, ensure_ascii=False)

        with open(self.reservation_file, "w", encoding="utf-8") as f:
            data = [r.to_dict() for r in manager.reservations]
            json.dump(data, f, indent=4, ensure_ascii=False)

    def load(self, manager):
        if os.path.exists(self.passenger_file):
            try:
                with open(self.passenger_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                manager.passengers = [Passenger.from_dict(item) for item in data]
            except json.JSONDecodeError:
                manager.passengers = []
        else:
            manager.passengers = []
            
        if os.path.exists(self.flight_file):
            try:
                with open(self.flight_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                manager.flights = [Flight.from_dict(item) for item in data]
            except json.JSONDecodeError:
                manager.flights = []
        else:
            manager.flights = []

        if os.path.exists(self.reservation_file):
            try:
                with open(self.reservation_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                manager.reservations = [Reservation.from_dict(item) for item in data]
            except json.JSONDecodeError:
                manager.reservations = []
        else:
            manager.reservations = []