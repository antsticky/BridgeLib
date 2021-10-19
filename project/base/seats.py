from enum import Enum


class Seat(Enum):
    N = 1
    E = 2
    S = 3
    W = 4
    
    def __next__(self):
        if self.value < 4:
            return Seat(self.value + 1)
        elif self.value == 4:
            return Seat(1)
        else:
            raise KeyError("Cannot find Seat")

    @property
    def partner(self):
        if self.name == "N":
            return Seat.S
        elif self.name == "E":
            return Seat.W
        elif self.name == "S":
            return Seat.N
        elif self.name == "W":
            return Seat.E
        else:
            raise KeyError("Cannot find partner")

    @property
    def direction(self):
        if self.name in ["N", "S"]:
            return [Seat.N, Seat.S]
        elif self.name in ["E", "W"]:
            return [Seat.E, Seat.W]
        else:
            raise KeyError("Seat cannot be found")
