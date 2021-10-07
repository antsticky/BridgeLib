class CardSuit:
    def __init__(self, name):
        self.name = name

    @property
    def value(self):
        if self.name == "spade":
            return 4
        elif self.name == "heart":
            return 3
        elif self.name == "diamond":
            return 2
        elif self.name == "club":
            return 1
        else:
            raise KeyError("Unknown suit")

    def __hash__(self):
        return hash(self.name) ^ hash(self.value)

    def __eq__(self, other):
        return all([self.name == other.name, self.value == other.value])

    def __lt__(self, other):
        if not isinstance(other, CardSuit):
            raise NotImplementedError("other is not a CardSuit")

        return self.value < other.value

    def __gt__(self, other):
        if not isinstance(other, CardSuit):
            raise NotImplementedError("other is not a CardSuit")

        return self.value > other.value

    @property
    def short_name(self):
        return self.name[0].upper()


class CardValue:
    def __init__(self, name, rank):
        self.display_name = name
        self.rank = rank

    def __eq__(self, other):
        return all([self.display_name == other.display_name, self.rank == other.rank])

    def __gt__(self, other):
        if not isinstance(other, CardValue):
            raise NotImplementedError("other is not a CardValue")

        return self.rank > other.rank

    def __lt__(self, other):
        if not isinstance(other, CardValue):
            raise NotImplementedError("other is not a CardValue")

        return self.rank < other.rank


class Card:
    def __init__(self, suit, value, visible=True, played=False):
        self.suit = suit
        self.value = value
        self.visible = visible
        self.played = played

    def __eq__(self, other):
        return all([self.suit == other.suit, self.value == other.value])

    def __gt__(self, other):
        if not isinstance(other, Card):
            raise NotImplementedError("other is not a Card")
        elif self.suit > other.suit:
            return True
        elif self.suit < other.suit:
            return False
        else:
            return self.value > other.value

    def __lt__(self, other):
        if not isinstance(other, Card):
            raise NotImplementedError("other is not a Card")
        elif self.suit < other.suit:
            return True
        elif self.suit > other.suit:
            return False
        else:
            return self.value < other.value
