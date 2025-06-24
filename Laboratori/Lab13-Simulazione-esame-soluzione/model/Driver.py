from dataclasses import dataclass

@dataclass
class Driver:
    driverID: int
    name: str
    surname: str

    def __hash__(self):
        return hash(self.driverID)

    def __str__(self):
        return f"{self.surname}"