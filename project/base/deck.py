from project.base.seats import Seat
from project.base.card import Card, CardSuit, CardValue
from project.base.logger import color_printer


class Deck:
    def __init__(self, N=None, S=None, E=None, W=None):
        self.N = N
        self.S = S
        self.E = E
        self.W = W

    @staticmethod
    def group_cards_by_suit(cards):
        hand = {i: [] for i in CardSuit.suits()}

        for card in cards:
            hand[card.suit].append(card)

        return hand

    @staticmethod
    def get_hand_max_suit(hand):
        return max([len(cards) for suit, cards in hand.items() if isinstance(suit, CardSuit)])

    @staticmethod
    def show_hand(hand, pre_space=0, show_played=False):
        for suit in CardSuit.suits_reverse():
            if pre_space != 0:
                print(pre_space * " ", end="")
            print(suit.short_name, end=": ")
            for card in hand[suit]:
                if show_played:
                    if card.played:
                        color_printer(card.value.display_name)
                    else:
                        print(card.value.display_name, end="")
                elif not card.played:
                    print(card.value.display_name, end="")
                else:
                    print(" ", end="")
            print()

    @staticmethod
    def show_opener_hand(board, declarer_str):
        decl = Seat[declarer_str]
        opener_hand = getattr(board.deck, next(decl).name)
        Deck.show_hand(opener_hand)

        return next(decl)

    @staticmethod
    def show_hands(hand1, hand2, hand1_max_len=0, orientation="vertical", space=0, show_played=False):
        if orientation == "horizontal":
            Deck.show_horizontal_hands(hand1, hand2, hand1_max_len, space, show_played)

        elif orientation == "vertical":
            Deck.show_vertical_hands(hand1, hand2, space)
        else:
            raise NotImplementedError

    @staticmethod
    def show_vertical_hands(hand1, hand2, space):
        Deck.show_hand(hand1)
        print(end="\n" * space)
        Deck.show_hand(hand2)

    @staticmethod
    def show_horizontal_hands(hand1, hand2, hand1_max_len, space, show_played):
        for suit in CardSuit.suits_reverse():
            print(suit.short_name, end=": ")
            for card in hand1[suit]:
                if show_played:
                    if card.played:
                        color_printer(card.value.display_name)
                    else:
                        print(card.value.display_name, end="")
                elif not card.played:
                    print(card.value.display_name, end="")
                else:
                    print(" ", end="")

            print((hand1_max_len - len(hand1[suit])) * " " + space * " ", end="")

            print(suit.short_name, end=": ")
            for card in hand2[suit]:
                if show_played:
                    if card.played:
                        color_printer(card.value.display_name)
                    else:
                        print(card.value.display_name, end="")

                elif not card.played:
                    print(card.value.display_name, end="")
                else:
                    print(" ", end="")

            print(end="\n")

    def show(self, show_played=True):
        max_NS = max(Deck.get_hand_max_suit(self.N), Deck.get_hand_max_suit(self.S)) + 2
        max_W = Deck.get_hand_max_suit(self.W) + 3

        Deck.show_hand(self.N, pre_space=max_W + 1, show_played=show_played)
        Deck.show_hands(self.W, self.E, hand1_max_len=max_W, space=max_NS, orientation="horizontal", show_played=show_played)
        Deck.show_hand(self.S, pre_space=max_W + 1, show_played=show_played)

    def sort(self, reverse=False):
        for attr in dir(self):
            val = getattr(self, attr)
            if isinstance(val, dict) and all(isinstance(k, CardSuit) and isinstance(v, list) for k, v in val.items()):
                try:
                    for suit in val:
                        val[suit].sort(reverse=(not reverse))
                except IndexError:
                    pass

    def save(self, file_name, write_type="w", played_cards=True):
        with open(file_name, write_type) as fp:
            for seat in Seat:
                if seat.value == 1:
                    fp.write(f"{seat.name}:")
                else:
                    fp.write(f";{seat.name}:")

                hand = getattr(self, seat.name)
                for suit in hand.keys():
                    for card in hand[suit]:
                        if played_cards:
                            fp.write(f"{card.suit.short_name}{card.value.display_name}")
                        else:
                            if not card.played:
                                fp.write(f"{card.suit.short_name}{card.value.display_name}")
            fp.write("\n")

    @staticmethod
    def load(file_name, line_idx):
        with open(file_name) as file:
            try:
                line = file.readlines()[line_idx]
            except IndexError:
                print(f"Board {line_idx} cannot be fount in file {file_name}")

            deck = {}
            for hand in line.replace("\n", "").split(";"):
                seat_name, cards = hand.split(":")
                deck[seat_name] = {k: [] for k in CardSuit.suits()}

                for card in map("".join, zip(*[iter(cards)] * 2)):
                    suit_name, value_name = card[0], card[1]
                    card_suit = CardSuit.create_by_short_name(suit_name)
                    card_value = CardValue.create_by_display_name(value_name)
                    card = Card(suit=card_suit, value=card_value)

                    deck[seat_name][card_suit].append(card)

            return Deck(**deck)

    @classmethod
    def shuffle(cls):
        import itertools
        import random

        res = [Card(suit=i[0], value=i[1]) for i in list(itertools.product(CardSuit.suits(), CardValue.values()))]
        random.shuffle(res)

        n_dec = Deck.group_cards_by_suit(res[0:13])
        s_dec = Deck.group_cards_by_suit(res[13:26])
        e_dec = Deck.group_cards_by_suit(res[26:39])
        w_dec = Deck.group_cards_by_suit(res[39:52])

        deck = cls(N=n_dec, S=s_dec, E=e_dec, W=w_dec)

        return deck
