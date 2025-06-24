from dataclasses import dataclass

@dataclass
class ConstructorStanding:
    constructorStandingsId: int
    raceId: int
    constructorId: int
    points: float
    position: int
    positionText: str
    wins: int

    def __hash__(self):
        return hash(self.constructorStandingsId)

    def __str__(self):
        return f"Standing {self.constructorStandingsId} – Constructor {self.constructorId}, Pos: {self.position}, Wins: {self.wins}, Points: {self.points}"
