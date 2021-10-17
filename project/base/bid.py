from enum import Enum

BASE_TRICK = 6


class GAMEBONUS(Enum):
    VUL = 450
    NONVUL = 250


class SLEMBONUS(Enum):
    VUL = 750
    NONVUL = 500


class mSUITVALUE(Enum):
    FIRST = 20
    SECOND = 20


class MSUITVALUE(Enum):
    FIRST = 30
    SECOND = 30


class NTSUITVALUE(Enum):
    FIRST = 40
    SECOND = 30


class SUITVALUE(Enum):
    C = mSUITVALUE
    D = mSUITVALUE
    H = MSUITVALUE
    S = MSUITVALUE
    NT = NTSUITVALUE


class BONUS(Enum):
    GAME = GAMEBONUS
    SLEM = SLEMBONUS
    GRAND_SLEM = SLEMBONUS


class GAMELEVEL(Enum):
    C = 5
    D = 5
    H = 4
    S = 4
    NT = 3


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
    def __init__(self, decl, bid, is_dbl, is_rdbl, vul="NONVUL"):
        # TODO: is_vul set in the bidding phase from the board setup
        self.decl = decl
        self.bid = bid
        self.is_dbl = is_dbl
        self.is_rdbl = is_rdbl

        if vul not in ["NONVUL", "VUL"]:
            raise ValueError("score must be one of NONVUL or VUL")

        self.vul = vul

        # add overtricks, trick_level, bidkey, etc here

    def bonus_value(self, suit_key, game_mlpy=1):
        bonus_value = 0
        if game_mlpy * self.bid.level >= GAMELEVEL[suit_key].value:
            bonus_value += BONUS.GAME.value[self.vul].value

        if self.bid.level >= 6:
            bonus_value += BONUS.SLEM.value[self.vul].value

        if self.bid.level == 7:
            bonus_value += BONUS.GRAND_SLEM.value[self.vul].value

        return bonus_value

    def make_value(self, tricks):
        if self.is_rdbl:
            return self.rdbl_make_value(tricks)
        elif self.is_dbl:
            return self.dbl_make_value(tricks)

        return self.plain_make_value(tricks)

    def base_value(self, suit_key, trick_level, level_mltpy=1):
        base_value = 50

        base_value += level_mltpy * SUITVALUE[suit_key].value.FIRST.value
        base_value += level_mltpy * (trick_level - 1) * SUITVALUE[suit_key].value.SECOND.value

        return base_value

    def undertrick_value(self, down_trikcs):
        if self.is_rdbl:
            return self.rdbl_down_value(down_trikcs)
        elif self.is_dbl:
            return self.dbl_down_value(down_trikcs)

        return self.plain_down_value(down_trikcs)

    def plain_down_value(self, down_trikcs):
        if self.vul == "NONVUL":
            return -50 * down_trikcs
        elif self.vul == "VUL":
            return -100 * down_trikcs

        raise KeyError("VUL type is unknown")

    def dbl_down_value(self, down_trikcs):
        if self.vul == "NONVUL":
            n1 = down_trikcs - 1
            n2 = down_trikcs - 3 if (down_trikcs - 3) > 0 else 0
            return -100 - 200 * n1 - 100 * n2
        elif self.vul == "VUL":
            return -300 * down_trikcs + 100

        raise KeyError("VUL type is unknown")

    def rdbl_down_value(self, down_trikcs):
        if self.vul == "NONVUL":
            n1 = down_trikcs - 1
            n2 = down_trikcs - 3 if (down_trikcs - 3) > 0 else 0
            return -200 - 400 * n1 - 200 * n2
        elif self.vul == "VUL":
            return -600 * down_trikcs + 200

        raise KeyError("VUL type is unknown")

    def plain_make_value(self, tricks):
        suit_key = self.bid.suit.short
        trick_level = tricks - BASE_TRICK

        value = self.base_value(suit_key, trick_level)
        value += self.bonus_value(suit_key)

        return value

    def dbl_make_value(self, tricks):
        over_trick_value = 100 if self.vul == "NONVUL" else 200
        tricks_level = tricks - BASE_TRICK
        over_tricks = tricks_level - self.bid.level

        suit_key = self.bid.suit.short

        value = 2 * self.base_value(suit_key, self.bid.level)
        value += over_tricks * over_trick_value
        value += self.bonus_value(suit_key, game_mlpy=2)

        return value

    def rdbl_make_value(self, tricks):
        over_trick_value = 200 if self.vul == "NONVUL" else 400
        success_penalty = 100

        tricks_level = tricks - BASE_TRICK
        over_tricks = tricks_level - self.bid.level

        suit_key = self.bid.suit.short

        value = self.base_value(suit_key, self.bid.level, level_mltpy=4)
        value += success_penalty
        value += over_tricks * over_trick_value
        value += self.bonus_value(suit_key, game_mlpy=4)

        return value

    def value(self, tricks=None):
        # TODO: hardcoded 6
        tricks = (self.bid.level + BASE_TRICK) if tricks is None else tricks

        if tricks < (self.bid.level + BASE_TRICK):
            return self.undertrick_value(self.bid.level + BASE_TRICK - tricks)

        return self.make_value(tricks)

    def __str__(self):
        retr_str = f"{self.decl.name}: {self.bid.name}"
        retr_str += "x" if self.is_dbl else ""
        retr_str += "x" if self.is_rdbl else ""

        return retr_str
