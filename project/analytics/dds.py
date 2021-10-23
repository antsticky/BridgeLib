import ctypes

import project.analytics.dds_project.examples.dds as dds


class DDSolver:
    # TODO: clean up
    dcardSuit = ["S", "H", "D", "C", "NT"]
    dcardHand = ["N", "E", "S", "W"]
    trump_index_dict = {"S": 0, "H": 1, "D": 2, "C": 3, "NT": 4}
    name_index_dict = {"N": 0, "E": 1, "S": 2, "W": 3}
    dbitMapRank = [0x0000, 0x0000, 0x0001, 0x0002, 0x0004, 0x0008, 0x0010, 0x0020, 0x0040, 0x0080, 0x0100, 0x0200, 0x0400, 0x0800, 0x1000, 0x2000]
    dcardRank = ["x", "x", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]

    def __init__(self):
        pass

    @staticmethod
    def get_trump_index(short_name):
        return DDSolver.trump_index_dict[short_name]

    @staticmethod
    def get_player_index(name):
        return DDSolver.name_index_dict[name]

    @staticmethod
    def get_card_pointer(rank):
        pointers = [0x0004, 0x0008, 0x0010, 0x0020, 0x0040, 0x0080, 0x0100, 0x0200, 0x0400, 0x0800, 0x1000, 0x2000, 0x4000]
        return pointers[rank - 1]

    @staticmethod
    def get_player_hand(deck, player):
        hand = getattr(deck, player)

        result = []
        result.append(DDSolver.get_hand_suit_value(hand, "S"))
        result.append(DDSolver.get_hand_suit_value(hand, "H"))
        result.append(DDSolver.get_hand_suit_value(hand, "D"))
        result.append(DDSolver.get_hand_suit_value(hand, "C"))

        return result

    @staticmethod
    def get_hand_suit_value(hand, suit_short_name):
        cards = [v for k, v in hand.items() if k.short_name == suit_short_name][0]
        pointers = [DDSolver.get_card_pointer(card.value.rank) for card in cards if card.played == False]
        if len(pointers) == 0:
            return None
        else:
            return sum(pointers)

    def prepare_holdings(self, deck):
        hands = {}
        for player in DDSolver.name_index_dict.keys():
            hands[player] = DDSolver.get_player_hand(deck, player)

        holdings = []
        for suit in range(4):
            suit_pointers = []
            for player in DDSolver.dcardHand:
                suit_pointers.append(hands[player][suit])
            holdings.append(suit_pointers)

        return holdings

    def equals_to_string(self, equals, res):
        p = 0
        m = equals >> 2
        for i in range(15, 1, -1):
            if m & int(DDSolver.dbitMapRank[i]):
                res[p] = bytes(DDSolver.dcardRank[i], "ascii")
                p = p + 1
        res[p] = 0

    def prepare_results(self, fut, title=None, is_print=True):
        if is_print:
            print("{}\n".format(title))
            print("{:6s} {:<6s} {:<6s} {:<6s} {:<6s}".format("card", "suit", "rank", "equals", "score"))

        score_table = {}
        for i in range(fut.contents.cards):
            res = ctypes.create_string_buffer(15)

            score = fut.contents.score[i]
            suit = DDSolver.dcardSuit[fut.contents.suit[i]]
            card = DDSolver.dcardRank[fut.contents.rank[i]]

            self.equals_to_string(fut.contents.equals[i], res)
            if is_print:
                print("{:6} {:<6s} {:<6s} {:<6s} {:<6}".format(i, suit, card, res.value.decode("utf-8"), score))

            if score not in score_table.keys():
                score_table[score] = []

            score_table[score].append((suit, card))

            for eqv in res.value.decode("utf-8"):
                score_table[score].append((suit, eqv))

            pass
        print()
        return score_table

    def run_solver(self, trump_index, first_player_index, holdings):
        dl = dds.deal()
        fut3 = dds.futureTricks()

        threadIndex = 0
        line = ctypes.create_string_buffer(80)

        dds.SetMaxThreads(0)

        dl.trump = trump_index
        dl.first = first_player_index

        dl.currentTrickSuit[0] = 0
        dl.currentTrickSuit[1] = 0
        dl.currentTrickSuit[2] = 0

        dl.currentTrickRank[0] = 0
        dl.currentTrickRank[1] = 0
        dl.currentTrickRank[2] = 0

        for h in range(dds.DDS_HANDS):
            for s in range(dds.DDS_SUITS):
                if holdings[s][h] is not None:
                    dl.remainCards[h][s] = holdings[s][h]

        target = -1  # No target; find all results
        solutions = 3  # Return all solutions
        mode = 0  # The way dds internally handles the last trick
        res = dds.SolveBoard(dl, target, solutions, mode, ctypes.pointer(fut3), threadIndex)
        return fut3, line, res

    def error_check(self, line, res):
        if res != dds.RETURN_NO_FAULT:
            dds.ErrorMessage(res, line)
            print("DDS error: {}".format(line.value.decode("utf-8")))

    def score_leads(self, deck, trump, first):
        trump_index = DDSolver.get_trump_index(trump.short)
        first_player_index = DDSolver.get_player_index(first.name)
        holdings = self.prepare_holdings(deck)

        fut3, line, res = self.run_solver(trump_index, first_player_index, holdings)
        self.error_check(line, res)
        score_table = self.prepare_results(ctypes.pointer(fut3), is_print=False)

        nb_solutions = sum([len(x) for x in list(score_table.values())])
        return score_table, nb_solutions
