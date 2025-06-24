from dataclasses import dataclass

@dataclass
class Result:
    raceId: int
    year: int
    round: int
    circuitId: int
    name: str
    date: str
    time: str
    url: str

    def __hash__(self):
        return hash((self.raceId, self.round))

    def __str__(self):
        return f"Result – {self.name} ({self.year})"
