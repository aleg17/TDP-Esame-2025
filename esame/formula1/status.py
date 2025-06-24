from dataclasses import dataclass

@dataclass
class Status:
    statusId: int
    status: str

    def __hash__(self):
        return hash(self.statusId)

    def __str__(self):
        return f"Status {self.statusId}: {self.status}"
