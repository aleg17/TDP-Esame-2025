from dataclasses import dataclass

@dataclass
class Race:
    raceId: int
    year: int
    round: int
    circuitId: int
    name: str
    date: str
    time: str
    url: str

    def __hash__(self):
        return hash(self.raceId)

    def __str__(self):
        return f"{self.year} – {self.name} ({self.date})"
