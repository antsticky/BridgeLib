from enum import Enum

from project.base.deck import Deck
from project.base.seats import Seat
from project.base.people import TablePlayers
from project.base.bid import BidsClass, Bid, BidSuit
from project.base.card import Card, CardSuit, CardValue


class PhaseClass(Enum):
    NEW = 0
    BID = 1
    PLAY = 2
    END = 3
    ABORTED = 4

    def __lt__(self, other):
        if not isinstance(other, PhaseClass):
            raise NotImplementedError("other is not a PhaseClass")

        return self.value < other.value

    def __gt__(self, other):
        if not isinstance(other, PhaseClass):
            raise NotImplementedError("other is not a PhaseClass")

        return self.value > other.value

    def __eq__(self, other):
        if not isinstance(other, PhaseClass):
            raise NotImplementedError("other is not a PhaseClass")

        return self.value == other.value


class Board:
    def __init__(self, board_nb, dealer=None):
        self.phase = PhaseClass.NEW
        self.board_nb = board_nb
        self.players = None

        self.dealer = Seat[dealer] if dealer is not None else Seat(board_nb % 4 or 4)
        self.active_player = self.dealer

        self.deck = None
        self.bids = BidsClass(
            dealer=self.dealer,
            callbacks={"board_contract": self.set_contract, "set_phase": self.set_phase_by_key, "increase_active_player": self.increase_active_player, "is_vul": self.is_vul},
        )
        self._contract = None
        self.dds = None

        self.plays = None
        self.nb_tricks = None

        self.claim = None

    @property
    def is_vul(self):
        # TODO: integrate to contract calculator
        base_bd_nb = self.board_nb

        while base_bd_nb > 16:
            base_bd_nb -= 16

        NS_vul = "VUL" if base_bd_nb in [2, 4, 5, 7, 10, 12, 13, 15] else "NONVUL"
        EW_vul = "VUL" if base_bd_nb in [3, 4, 6, 7, 9, 10, 13, 16] else "NONVUL"

        return {"N": NS_vul, "S": NS_vul, "E": EW_vul, "W": EW_vul}

    @property
    def contract(self):
        if self.phase < PhaseClass.PLAY:
            raise ValueError("Do bidding first")

        return self._contract

    @contract.setter
    def contract(self, contr):
        self.set_contract(contr)

    def set_contract(self, value):
        self._contract = value

    def set_phase_by_key(self, key):
        self.phase = PhaseClass[key]

    def increase_active_player(self, seat):
        self.active_player = next(seat)

    @staticmethod
    def get_active_player_by_trick(trick, trump):
        player_won, card_won = trick[0]
        lead_suit = card_won.suit

        key_suits = [lead_suit] if trump == BidSuit.from_str("NT") else [lead_suit, trump]
        my_trump = trump if trump != BidSuit.from_str("NT") else None

        for player, card in trick:
            if card.suit in key_suits:
                if card_won.suit == card.suit:
                    if card_won.value < card.value:
                        card_won = card
                        player_won = player
                elif (my_trump is not None) and card.suit == trump:
                    card_won = card
                    player_won = player

        return player_won

    def deal(self):
        if self.phase == PhaseClass.NEW:
            self.deck = Deck.shuffle()
            self.set_phase_by_key("BID")
        else:
            print("Deal was alredy made, please use redeal")

    def load_deck(self, file_name, line_idx=0):
        self.deck = Deck.load(file_name=file_name, line_idx=line_idx)
        self.phase = PhaseClass.BID
        # TODO make reset actions when go back in phase function(cur_phase, new_phase)

    def redeal(self):
        # TODO: Implement this
        raise NotImplementedError("NOT implemented")

    def seating(self, N, S, E, W):
        self.players = TablePlayers(N=N, S=S, E=E, W=W)

    def bid(self, bid, seat):
        if self.active_player != Seat[seat]:
            print("It is not your turn")
        elif self.phase == PhaseClass.BID:
            self.bids.bidding(Bid(bid), Seat[seat])
        elif self.phase == PhaseClass.NEW:
            print("Deal first")
        else:
            print("Bidding was already made")

    def play(self, card, seat):
        if self.active_player != Seat[seat]:
            print("It is not your turn")
        elif self.phase == PhaseClass.PLAY:
            player = Seat[seat]
            suit = CardSuit.create_by_short_name(card[0].upper())
            value = CardValue.create_by_display_name(card[1:].upper())
            played_card = Card(suit, value)

            player_hand = getattr(self.deck, player.name)
            player_suit_cards = player_hand[suit]

            if not self.check_is_valid_play(card, seat, played_card, player_suit_cards):
                return -1

            self.valid_play_actions(player, played_card, player_suit_cards)

        else:
            # TODO: be more concrete
            print("Not bidding phase...")

    def valid_play_actions(self, player, played_card, player_suit_cards):
        list(filter(lambda x: x == played_card, player_suit_cards))[0].played = True

        self.store_play(player, played_card)

        if len(self.plays) % 4 != 0:
            self.increase_active_player(player)
        else:
            trick = self.plays[-4:]

            active_player = self.get_active_player_by_trick(trick, self.contract.bid.suit)

            self.active_player = active_player
            self.update_nb_tricks(active_player)

            if sum(self.nb_tricks.values()) == 13:
                self.close_play_phase(active_player)

    def close_play_phase(self, active_player):
        self.contract.decl_tricks = self.nb_tricks[active_player.name] + self.nb_tricks[active_player.partner.name]
        self.phase = PhaseClass.END

    def update_nb_tricks(self, active_player):
        if self.nb_tricks is None:
            self.nb_tricks = {"N": 0, "E": 0, "W": 0, "S": 0}
        self.nb_tricks[active_player.name] += 1

    def store_play(self, player, played_card):
        if self.plays is None:
            self.plays = []

        self.plays.append((player, played_card))

    def check_is_valid_play(self, card, seat, played_card, player_suit_cards):
        if played_card not in player_suit_cards:
            print(f"Player {seat} does not holds the given card ({card})")
            return False
        elif list(filter(lambda x: x == played_card, player_suit_cards))[0].played:
            print(f"The card {card} is already played")
            return False

        return True
