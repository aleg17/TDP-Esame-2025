from dataclasses import dataclass

@dataclass
class PitStop:
    raceId: int
    driverId: int
    stop: int
    lap: int
    time: str
    duration: str
    milliseconds: int

    def __hash__(self):
        return hash((self.raceId, self.driverId, self.stop))

    def __str__(self):
        return f"Pit Stop {self.stop} – Driver {self.driverId}, Lap {self.lap}, Duration: {self.duration}"
