from dataclasses import dataclass

@dataclass
class DriverStanding:
    driverStandingsId: int
    raceId: int
    driverId: int
    points: float
    position: int
    positionText: str
    wins: int

    def __hash__(self):
        return hash(self.driverStandingsId)

    def __str__(self):
        return f"Standing {self.driverStandingsId} – Driver {self.driverId}, Pos: {self.position}, Wins: {self.wins}, Points: {self.points}"
