from enum import Enum

class SeatDirections(Enum):
    N = 1
    E = 2
    S = 3
    W = 4

    @property
    def partner(self):
        if self.name == "N":
            return SeatDirections.S
        elif self.name == "E":
            return SeatDirections.W
        elif self.name == "S":
            return SeatDirections.N
        elif self.name == "W":
            return SeatDirections.E
        else:
            raise KeyError("Cannot find partner")