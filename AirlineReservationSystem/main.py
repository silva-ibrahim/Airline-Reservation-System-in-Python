from datetime import datetime
from airline_manager import AirlineManager
from storage import Storage


def get_required_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty. Please try again.")


def show_menu():
    print("\n--------FLIGHT RESERVATION SYSTEM--------\n")
    print("1. Add passenger")
    print("2. Add flight")
    print("3. List passengers")
    print("4. List flights")
    print("5. Search flights")
    print("6. Create reservation")
    print("7. List reservations")
    print("8. Cancel reservation")
    print("9. Flight statistics")
    print("10. Exit")


def add_passenger(manager, storage):
    print("\n--- ADD PASSENGER ---")

    name = get_required_input("First name: ")
    surname = get_required_input("Last name: ")
    email = get_required_input("Email: ")
    phone = get_required_input("Phone: ")
    passport = get_required_input("Passport number: ")

    passenger = manager.add_passenger(name, surname, email, phone, passport)
    storage.save(manager)
    print("\nPassenger added successfully.")
    print(f"Passenger ID: {passenger.passenger_id}")


def add_flight(manager, storage):
    print("\n--- ADD FLIGHT ---")
    flight_number = get_required_input("Flight number: ").upper()

    if manager.find_flight(flight_number):
        print("This flight number is already in use.")
        return

    departure = get_required_input("Departure city: ")
    destination = get_required_input("Destination city: ")

    while True:
        date = get_required_input("Date (DD/MM/YYYY): ")
        try:
            flight_date = datetime.strptime(date,"%d/%m/%Y")
            if flight_date.date() < datetime.now().date():
                print(
                    "You cannot select a date in the past."
                )
                continue
            break
        except ValueError:
            print("Invalid date. Example: 25/08/2026")

    time = get_required_input("Time: ")
    aircraft = get_required_input("Aircraft: ")

    while True:
        price_input = get_required_input("Ticket price: ")
        try:
            price = float(price_input)
            if price <= 0:
                print("Ticket price must be greater than 0.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    flight = manager.add_flight(flight_number, departure, destination, date, time, aircraft, price)
    storage.save(manager)
    print(f"\nFlight {flight.flight_number} was added successfully.")


def list_passengers(manager):
    
    print("\n--- PASSENGERS ---")
    if not manager.passengers:
        print("No registered passengers found.")
        return

    for passenger in manager.passengers:
        print(
            f"{passenger.passenger_id} | "
            f"{passenger.get_full_name()} | "
            f"{passenger.email} | "
            f"Passport: {passenger.passport_number}"
        )


def list_flights(manager):
    print("\n--- FLIGHTS ---")

    if not manager.flights:
        print("No registered flights found.")
        return

    for flight in manager.flights:
        print(
            f"{flight.flight_number} | "
            f"{flight.departure} -> "
            f"{flight.destination} | "
            f"{flight.date} {flight.time} | "
            f"${flight.price:.2f} | "
            f"Available seats: "
            f"{flight.available_seat_count()} | "
            f"{flight.status}"
        )


def search_flights(manager):
    print("\n--- SEARCH FLIGHTS ---")
    departure = get_required_input("Departure city: ")
    destination = get_required_input("Destination city: ")
    date = get_required_input("Date (DD/MM/YYYY): ")

    results = manager.search_flights(departure, destination, date)

    if not results:
        print("\nNo suitable flights found.")
        return

    print("\n--- AVAILABLE FLIGHTS ---")
    for flight in results:
        print(
            f"{flight.flight_number} | "
            f"{flight.departure} -> "
            f"{flight.destination} | "
            f"{flight.time} | "
            f"${flight.price:.2f} | "
            f"{flight.available_seat_count()} "
            f"available seats"
        )


def show_seats(flight):
    print("\n--- SEAT PLAN ---")
    print("O = Available")
    print("X = Occupied\n")

    columns = ["A", "B", "C", "D", "E", "F"]
    print("     " + "   ".join(columns))

    for row in range(1, 11):
        seats = []
        for column in columns:
            seat_number = f"{row}{column}"
            if flight.seats[seat_number] == "Available":
                seats.append("O")
            else:
                seats.append("X")
        print(f"{row:2}   " + "   ".join(seats))


def create_reservation(manager, storage):
    print("\n--- CREATE RESERVATION ---")
    passenger_id = get_required_input("Passenger ID: ").upper()
    passenger = manager.find_passenger(passenger_id)
    if passenger is None:
        print("Passenger not found.")
        return

    flight_number = get_required_input("Flight number: ").upper()
    flight = manager.find_flight(flight_number)
    if flight is None:
        print("Flight not found.")
        return

    show_seats(flight)
    seat_number = get_required_input("\nSelect a seat (e.g., 1A, 4B): ").upper()

    reservation, message = manager.create_reservation( passenger_id, flight_number, seat_number)
    print(f"\n{message}")

    if reservation:
        storage.save(manager)
        print("\n" + "=" * 40)
        print("        RESERVATION DETAILS")
        print("=" * 40)
        print(f"Reservation ID : " f"{reservation.reservation_id}")
        print(f"Passenger      : " f"{passenger.get_full_name()}")
        print(f"Flight         : " f"{reservation.flight_number}")
        print(f"Seat           : " f"{reservation.seat_number}")
        print(f"Price          : ${reservation.price:.2f}")
        print(f"Status         : " f"{reservation.status}")
        print("=" * 40)


def list_reservations(manager):
    print("\n--- ACTIVE RESERVATIONS ---")
    active_reservations = [reservation for reservation in manager.reservations if reservation.status == "Confirmed"]

    if not active_reservations:
        print("No active reservations found.")
        return

    for reservation in active_reservations:
        passenger = manager.find_passenger(reservation.passenger_id)
        if passenger:
            passenger_name = (passenger.get_full_name())
        else:
            passenger_name = "Unknown"

        print(
            f"{reservation.reservation_id} | "
            f"{passenger_name} | "
            f"Flight: {reservation.flight_number} | "
            f"Seat: {reservation.seat_number} | "
            f"${reservation.price:.2f} | "
            f"{reservation.status}"
        )


def cancel_reservation(manager, storage):
    print("\n--- CANCEL RESERVATION ---")
    reservation_id = get_required_input("Reservation ID (e.g., RES-0003 or 3): ").upper()

    if reservation_id.isdigit():
        reservation_id = (f"RES-{int(reservation_id):04d}")

    success, message = (manager.cancel_reservation(reservation_id))
    print(f"\n{message}")
    if success:
        storage.save(manager)


def show_statistics(manager):
    print("\n--- FLIGHT STATISTICS ---")
    total_flights = len(manager.flights)
    scheduled_flights = sum(1 for flight in manager.flights if flight.status == "Scheduled")
    cancelled_flights = sum(1 for flight in manager.flights if flight.status == "Cancelled")
    confirmed_reservations = (manager.total_confirmed_reservations())
    revenue = manager.total_revenue()

    total_seats = sum(len(flight.seats) for flight in manager.flights)
    available_seats = sum(flight.available_seat_count() for flight in manager.flights)
    reserved_seats = (total_seats - available_seats)

    print(f"Total flights          : " f"{total_flights}")
    print(f"Scheduled flights      : " f"{scheduled_flights}")
    print(f"Cancelled flights      : " f"{cancelled_flights}")
    print(f"Confirmed reservations : " f"{confirmed_reservations}")
    print(f"Total seats            : " f"{total_seats}")
    print(f"Occupied seats         : " f"{reserved_seats}")
    print(f"Available seats        : " f"{available_seats}")
    print(f"Total revenue          : " f"${revenue:.2f}")


def main():
    manager = AirlineManager()
    storage = Storage()
    storage.load(manager)

    print("\nWelcome to the Flight Reservation System!")

    while True:
        show_menu()
        choice = input("Select an option: ").strip()

        if choice == "1":
            add_passenger(manager, storage)
        elif choice == "2":
            add_flight(manager, storage)
        elif choice == "3":
            list_passengers(manager)
        elif choice == "4":
            list_flights(manager)
        elif choice == "5":
            search_flights(manager)
        elif choice == "6":
            create_reservation(manager, storage)
        elif choice == "7":
            list_reservations(manager)
        elif choice == "8":
            cancel_reservation(manager, storage)
        elif choice == "9":
            show_statistics(manager)
        elif choice == "10":
            storage.save(manager)
            print("\nData saved successfully.")
            print("Thank you for using the Flight Reservation System.")
            print("The program is shutting down...")
            break
        else:
            print("\nInvalid option.Please select a number between 1 and 10.")


if __name__ == "__main__":
    main()