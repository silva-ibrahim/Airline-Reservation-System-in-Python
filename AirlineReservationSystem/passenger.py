class Passenger:
    def __init__(self, passenger_id, name, surname, email, phone, passport_number):
        self.passenger_id = passenger_id
        self.name = name
        self.surname = surname
        self.email = email
        self.phone = phone
        self.passport_number = passport_number

    def get_full_name(self):
        return f"{self.name} {self.surname}"

    def to_dict(self):
        return {
            "passenger_id": self.passenger_id,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "phone": self.phone,
            "passport_number": self.passport_number
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["passenger_id"], data["name"], data["surname"],
            data["email"], data["phone"], data["passport_number"]
        )