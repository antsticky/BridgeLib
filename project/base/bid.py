from enum import Enum


class BidSuitNames(Enum):
    S = "spade"
    H = "heart"
    D = "diamond"
    C = "club"
    NT = "no-trump"


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


class BidsClass:
    def __init__(self, dealer, callbacks):
        self.dealer = dealer
        self._contract = None
        self.callbacks = callbacks
        self.bids = []

        self.nb_pass = 0
        self.is_dbl = False
        self.is_rdbl = False

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
        if self.nb_pass == 3:
            raise ValueError("Bidding ended")

        ###############################
        if bid.name == "p":
            self.nb_pass += 1
        else:
            self.nb_pass = 0
        ###############################
        if (bid.name == "x") and (self.nb_pass in [0, 2]):
            self.is_dbl = True
        elif bid.name == "x":
            raise ValueError("Cannot double this contract")
        ###############################
        if all([bid.name == "xx", self.is_dbl, self.nb_pass in [0, 2]]):
            self.is_rdbl = True
        elif bid.name == "xx":
            raise ValueError("Cannot double this contract")
        ###############################
        if bid.level is not None:
            self.is_dbl = False
            self.is_rdbl = False
        ###############################

        # TODO: check bid logics, is bid_old<bid_new and seat_old-seat_new = 1
        self.bids.append((bid, seat))

        if self.nb_pass == 3:
            cont_bid, cont_seat = self.bids[-4]
            declarer = self.get_declarer(cont_seat, cont_bid)
            self.contract = Contract(declarer, cont_bid, self.is_dbl, self.is_rdbl)
            self.callbacks.get("increase_active_player")(declarer)
        else:
            self.callbacks.get("increase_active_player")(seat)


class Bid:
    def __init__(self, bid_str):
        self.name = bid_str
        if bid_str in ["x", "p", "xx"]:
            self.level = None
            self.suit = None
        else:
            self.level = int("".join([i for i in bid_str if i.isnumeric()]))
            self.suit = BidSuit.from_str("".join([i for i in bid_str if not i.isnumeric()]))


class Contract:
    def __init__(self, decl, bid, is_dbl, is_rdbl):
        self.decl = decl
        self.bid = bid
        self.is_dbl = is_dbl
        self.is_rdbl = is_rdbl

    def __str__(self):
        retr_str = f"{self.decl.name}: {self.bid.name}"
        retr_str += "x" if self.is_dbl else ""
        retr_str += "x" if self.is_rdbl else ""

        return retr_str
