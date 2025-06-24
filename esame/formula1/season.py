from dataclasses import dataclass

@dataclass
class Season:
    raceId: int
    year: int

    def __hash__(self):
        return hash(self.raceId)

    def __str__(self):
        return f"Season {self.year}"
