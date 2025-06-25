from dataclasses import dataclass

@dataclass
class Driver:
    customer_id: int
    first_name: str: str
    last_name: str
    phone: str
    email: str
    street: str
    city: str
    state: str
    zip_code: int

    def __hash__(self):
        return hash(self.customer_id)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



