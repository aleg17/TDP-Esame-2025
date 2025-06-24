from dataclasses import dataclass

@dataclass
class ConstructorResult:
    constructorResultsId: int
    raceId: int
    constructorId: int
    points: float
    status: str

    def __hash__(self):
        return hash(self.constructorResultsId)

    def __str__(self):
        return f"Result {self.constructorResultsId} – Constructor {self.constructorId} in Race {self.raceId}: {self.points} pts, Status: {self.status}"
