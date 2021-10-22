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


class Contract:
    def __init__(self, decl, bid, is_dbl, is_rdbl, vul="NONVUL"):
        self.decl = decl
        self.bid = bid
        self.is_dbl = is_dbl
        self.is_rdbl = is_rdbl

        if vul not in ["NONVUL", "VUL"]:
            raise ValueError("score must be one of NONVUL or VUL")

        self.vul = vul
        self._decl_tricks = None

    def get_decl_tricks(self):
        if self._decl_tricks is None:
            raise ValueError("No tricks ara available")
        return self._decl_tricks

    def set_decl_tricks(self, direction_tricks):
        if direction_tricks < 0 or direction_tricks > 13:
            raise ValueError

        self._decl_tricks = direction_tricks

    def overtricks(self, tricks):
        return tricks - BASE_TRICK - self.bid.level

    decl_tricks = property(get_decl_tricks, set_decl_tricks)

    def bonus_value(self, game_mlpy=1):
        bonus_value = 0
        if game_mlpy * self.bid.level >= GAMELEVEL[self.bid.suit.short].value:
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

    def base_value(self, level, level_mltpy=1):
        base_value = 50

        base_value += level_mltpy * SUITVALUE[self.bid.suit.short].value.FIRST.value
        base_value += level_mltpy * (level - 1) * SUITVALUE[self.bid.suit.short].value.SECOND.value

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
        trick_level = tricks - BASE_TRICK

        value = self.base_value(trick_level)
        value += self.bonus_value()

        return value

    def dbl_make_value(self, tricks):
        over_trick_value = 100 if self.vul == "NONVUL" else 200

        value = 2 * self.base_value(self.bid.level)
        value += self.overtricks(tricks) * over_trick_value
        value += self.bonus_value(game_mlpy=2)

        return value

    def rdbl_make_value(self, tricks):
        over_trick_value = 200 if self.vul == "NONVUL" else 400
        success_penalty = 100

        value = self.base_value(self.bid.level, level_mltpy=4)
        value += success_penalty
        value += self.overtricks(tricks) * over_trick_value
        value += self.bonus_value(game_mlpy=4)

        return value

    def value(self, tricks=None):
        if tricks is not None:
            pass
        elif self.decl_tricks is not None:
            tricks = self.decl_tricks
        else:
            tricks = self.bid.level + BASE_TRICK

        if tricks < (self.bid.level + BASE_TRICK):
            return self.undertrick_value(self.bid.level + BASE_TRICK - tricks)

        return self.make_value(tricks)

    def __str__(self):
        retr_str = f"{self.decl.name}: {self.bid.name}"
        retr_str += "x" if self.is_dbl else ""
        retr_str += "x" if self.is_rdbl else ""

        return retr_str
