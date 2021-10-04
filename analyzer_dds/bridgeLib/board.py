from enum import Enum

from bridgeLib.deck import Deck
from bridgeLib.people import TablePlayers

class PhaseClass(Enum):
    NEW = "NEW"
    BID = "BID"
    PLAY = "PLAY"
    END = "END"
    ABORTED = "ABORTED"

class Board:
    def __init__(self, board_nb):
        self.phase = PhaseClass.NEW
        self.board_nb = board_nb

        self.tricks = None

        self.contract = None
        self.players = None
        self.dds = None
        self.deck = None
        self.bid = None
        self.play = None
        self.claim = None

    def deal(self):
        if self.phase == PhaseClass.NEW:
            self.deck = Deck.shuffle()
            self.phase = PhaseClass.BID
        else:
            print("Deal was alredy made, please use redeal")

    def load(self):
        pass

    def redeal(self):
        raise NotImplementedError("NOT implemented")

    def seating(self, N, S, E, W):
        self.players = TablePlayers(N=N, S=S, E=E, W=W)
