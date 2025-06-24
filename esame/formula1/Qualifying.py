from dataclasses import dataclass

@dataclass
class Qualifying:
    qualifyId: int
    raceId: int
    driverId: int
    constructorId: int
    number: int
    position: int
    q1: str
    q2: str
    q3: str

    def __hash__(self):
        return hash(self.qualifyId)

    def __str__(self):
        return f"Qualifying {self.qualifyId} – Driver {self.driverId}, Position {self.position}"
