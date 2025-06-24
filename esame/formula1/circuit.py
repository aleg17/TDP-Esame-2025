from dataclasses import dataclass

@dataclass
class Circuit:
    circuitId: int
    circuitRef: str
    name: str
    location: str
    country: str
    lat: float
    lng: float
    alt: float
    url: str

    def __hash__(self):
        return hash(self.circuitId)

    def __str__(self):
        return f"{self.name} – {self.location}, {self.country}"


