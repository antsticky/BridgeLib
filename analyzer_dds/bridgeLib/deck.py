from bridgeLib.card import Card, CardSuit, CardValue

SUIT_LIST = ["spade", "heart", "diamond", "club"]
CARD_VALUE_LIST = [CardValue(f"{i+2}", i + 1) for i in range(8)] + [CardValue(f"{i}", j) for i, j in {"T": 9, "J": 10, "Q": 11, "K": 12, "A": 13}.items()]


class Deck:
    suits = [CardSuit(i) for i in SUIT_LIST]
    values = CARD_VALUE_LIST

    def __init__(self, N=None, S=None, E=None, W=None):
        self.N = N
        self.S = S
        self.E = E
        self.W = W

    @staticmethod
    def group_cards(cards):
        hand = {i: [] for i in Deck.suits}

        for card in cards:
            hand[card.suit].append(card)

        return hand

    @staticmethod
    def get_hand_max_suit(hand):
        max_len = -1

        for suit in Deck.suits:
            len_i = len(hand[suit])
            if len_i > max_len:
                max_len = len_i

        return max_len

    @staticmethod
    def show_hand(hand, pre_space=0):
        for suit in Deck.suits:
            if pre_space != 0:
                print(pre_space * " ", end="")
            print(suit.short_name, end=": ")
            for card in hand[suit]:
                print(card.value.display_name, end="")
            print()

    @staticmethod
    def show_hands(hand1, hand2, hand1_max_len=0, orientation="vertical", space=0):
        if orientation == "horizontal":
            for suit in Deck.suits:
                print(suit.short_name, end=": ")
                for card in hand1[suit]:
                    print(card.value.display_name, end="")

                print((hand1_max_len - len(hand1[suit])) * " " + space * " ", end="")

                print(suit.short_name, end=": ")
                for card in hand2[suit]:
                    print(card.value.display_name, end="")

                print(end="\n")

        elif orientation == "vertical":
            Deck.show_hand(hand1)
            print(end="\n" * space)
            Deck.show_hand(hand2)
        else:
            raise NotImplemented

    def show(self):
        max_NS = max(Deck.get_hand_max_suit(self.N), Deck.get_hand_max_suit(self.S)) + 2
        max_W = Deck.get_hand_max_suit(self.W) + 3

        Deck.show_hand(self.N, pre_space=max_W + 1)
        Deck.show_hands(self.W, self.E, hand1_max_len=max_W, space=max_NS, orientation="horizontal")
        Deck.show_hand(self.S, pre_space=max_W + 1)

    def sort(self, reverse=False):
        for attr in dir(self):
            val = getattr(self, attr)
            if isinstance(val, dict) and all(isinstance(k, CardSuit) and isinstance(v, list) for k, v in val.items()):
                try:
                    for suit in val:
                        val[suit].sort(reverse=(not reverse))
                except:
                    pass

    @classmethod
    def shuffle(cls):
        import itertools
        import random

        res = [Card(suit=i[0], value=i[1]) for i in list(itertools.product(Deck.suits, Deck.values))]
        random.shuffle(res)

        n_dec = Deck.group_cards(res[0:13])
        s_dec = Deck.group_cards(res[13:26])
        e_dec = Deck.group_cards(res[26:39])
        w_dec = Deck.group_cards(res[39:52])

        deck = cls(N=n_dec, S=s_dec, E=e_dec, W=w_dec)

        return deck
