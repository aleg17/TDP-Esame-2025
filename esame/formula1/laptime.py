from dataclasses import dataclass

@dataclass
class LapTime:
    raceId: int
    driverId: int
    lap: int
    position: int
    time: str
    milliseconds: int

    def __hash__(self):
        return hash((self.raceId, self.driverId, self.lap))

    def __str__(self):
        return f"Lap {self.lap} – Driver {self.driverId} in Race {self.raceId}: {self.time} ({self.milliseconds} ms)"
