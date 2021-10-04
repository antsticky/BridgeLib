from enum import Enum

BASE_TRICKS = 6
BASE_SCORE = 50

class dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class NTClass(Enum):
    FIRST_TRICK = 40
    SECOND_TRICK = 30
    GAME_LEVEL = 3
    SLAM_LEVEL = 6
    GRAND_SLAM_LEVEL = 7

class MajorClass(Enum):
    FIRST_TRICK = 30
    SECOND_TRICK = 30
    GAME_LEVEL = 4
    SLAM_LEVEL = 6
    GRAND_SLAM_LEVEL = 7

class MinorClass(Enum):
    FIRST_TRICK = 20
    SECOND_TRICK = 20
    GAME_LEVEL = 5
    SLAM_LEVEL = 6
    GRAND_SLAM_LEVEL = 7

SpadeClass = MajorClass
HeartClass = MajorClass

DiamondClass = MinorClass
ClubClass = MinorClass

class CardRankClass:
    def __init__(self, name, rank):
        self.name = name
        self.rank = rank

class CardRank(Enum):
    ONE = 1
    TWO = 1


class Suits(Enum):
    NT = NTClass
    SPADE = SpadeClass
    HEART = HeartClass
    DIAMON = DiamondClass
    CLUB = ClubClass

    @property
    def first_trick(self):
        return self.value.FIRST_TRICK.value

    @property
    def second_trick(self):
        return self.value.SECOND_TRICK.value


class Bonus:
    def __init__(self, score):
        self.score = score
        self.game = "3"

class BaseTricks:
    def __init__(self, level, suit):
        self.suit = suit
  
        self.level = level
        self.tricks = level + BASE_TRICKS

    @property
    def value(self):
        return BASE_SCORE + self.suit.first_trick + (self.level - 1) * self.suit.second_trick

class Contract:
    def __init__(self, level, suit, tricks):
        self.base_tricks = BaseTricks(level, suit)
        self.suit = suit
        self.tricks = tricks
    
    @property
    def value(self):
        return 43



if __name__ == "__main__":
    nt = Contract(1, suit=Suits.NT, tricks=8)
    pass
    