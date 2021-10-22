from enum import Enum

from project.base.contract import Contract


class BidSuitNames(Enum):
    C = "club"
    D = "diamond"
    H = "heart"
    S = "spade"
    NT = "no-trump"

    def index(suit_key):
        return [e.name for e in BidSuitNames].index(suit_key)


class BidActions(Enum):
    P = "p"
    DBL = "x"
    RDBL = "xx"


class BidSuit:
    def __init__(self, suit):
        self.name = suit.value
        self.short = suit.name

    @classmethod
    def from_str(cls, suit_str):
        suit_cls = cls(BidSuitNames[suit_str.upper()])
        return suit_cls

    def __eq__(self, other):
        if all([self.name == other.name, self.short == other.short]):
            return True
        else:
            return False

    def __lt__(self, other):
        if not isinstance(other, BidSuit):
            raise NotImplementedError("other is not a BidSuit")

        return BidSuitNames.index(self.short) < BidSuitNames.index(other.short)

    def __gt__(self, other):
        if not isinstance(other, BidSuit):
            raise NotImplementedError("other is not a BidSuit")

        return BidSuitNames.index(self.short) > BidSuitNames.index(other.short)


class Bid:
    def __init__(self, bid_str):
        self.name = bid_str
        if bid_str in ["x", "p", "xx"]:
            self.level = None
            self.suit = None
        else:
            self.level = int("".join([i for i in bid_str if i.isnumeric()]))
            self.suit = BidSuit.from_str("".join([i for i in bid_str if not i.isnumeric()]))

    def __eq__(self, other):
        if not isinstance(other, Bid):
            raise NotImplementedError("other is not a Bid")

        return all([self.level == other.level, self.suit == other.suit])

    def __gt__(self, other):
        if other is None:
            return True

        if not isinstance(other, Bid):
            raise NotImplementedError("other is not a Bid")

        if all([other.suit, other.level]):
            return True

        if self.level == other.level:
            return self.suit > other.suit

        return self.level > other.level


class BidsClass:
    def __init__(self, dealer, callbacks):
        self.dealer = dealer
        self._contract = None
        self.callbacks = callbacks
        self.bids = []

        self.nb_pass = 0
        self.is_dbl = False
        self.is_rdbl = False

        self.last_bid_action = None
        self.last_valid_bid = None

    @property
    def contract(self):
        return self._contract

    @contract.setter
    def contract(self, value):
        self._contract = value

        if "board_contract" in self.callbacks.keys():
            self.callbacks.get("board_contract")(value)

        if "set_phase" in self.callbacks.keys():
            self.callbacks.get("set_phase")("PLAY")

    def get_declarer(self, cont_seat, cont_bid):
        pd = cont_seat.partner

        for bid_past, seat_past in self.bids:
            if seat_past in [cont_seat, pd]:
                if (bid_past.suit is not None) and (bid_past.suit == cont_bid.suit):
                    return seat_past

        raise ValueError("Dec. cannot be found")

    def show(self):
        bid_len_displ = 5
        print((self.dealer.value - 1) * (bid_len_displ + 3) * " ", end="")

        for i, bid in enumerate(self.bids):
            end_chr = "\n" if (bid[1].name == "W" or i == len(self.bids) - 1) else " - "
            displ = bid[0].name

            displ += " " * (bid_len_displ - len(displ))
            print(displ, end=end_chr)

    def bidding(self, bid, seat):
        self.detect_bid_end(bid)
        self.check_bid_validity(bid, seat)

        if bid.level is not None:
            self.is_dbl = False
            self.is_rdbl = False
            self.last_valid_bid = bid

        self.bids.append((bid, seat))
        self.last_bid_action = (bid, seat)

        if self.nb_pass == 3:
            self.close_bidding()
        else:
            self.callbacks.get("increase_active_player")(seat)

    def check_bid_validity(self, bid, seat):
        # Check whos turn is it
        if self.last_bid_action is None:
            assert seat == self.dealer, "It is not your turn"
        else:
            assert seat == next(self.last_bid_action[1]), "It is not your turn"

        # Check if double is available
        if (bid.name == BidActions.DBL.value) and (self.nb_pass in [0, 2]):
            self.is_dbl = True
        elif bid.name == BidActions.DBL.value:
            raise ValueError("Cannot double this contract")

        # Check if re-double is available
        if all([bid.name == BidActions.RDBL.value, self.is_dbl, self.nb_pass in [0, 2]]):
            self.is_rdbl = True
        elif bid.name == BidActions.RDBL.value:
            raise ValueError("Cannot re-double this contract")

        if not (bid > self.last_valid_bid):
            raise ValueError("The new bid do not meet with the bid_old<bid_new condition")

    def close_bidding(self):
        cont_bid, cont_seat = self.bids[-4]
        declarer = self.get_declarer(cont_seat, cont_bid)
        is_vul = self.callbacks.get("is_vul", {})[declarer.name]
        self.contract = Contract(decl=declarer, bid=cont_bid, is_dbl=self.is_dbl, is_rdbl=self.is_rdbl, vul=is_vul)
        self.callbacks.get("increase_active_player")(declarer)

    def detect_bid_end(self, bid):
        if self.nb_pass == 3:
            raise ValueError("Bidding ended")

        if bid.name == BidActions.P.value:
            self.nb_pass += 1
        else:
            self.nb_pass = 0
