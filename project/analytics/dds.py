import ctypes

import project.analytics.dds_project.examples.dds as dds


class BaseSolver:
    player_seats = ["N", "E", "S", "W"]
    trump_suits = ["S", "H", "D", "C", "NT"]
    trump_index_dict = {"S": 0, "H": 1, "D": 2, "C": 3, "NT": 4}
    name_index_dict = {"N": 0, "E": 1, "S": 2, "W": 3}

    def __init__(self):
        pass


class DDLeadSolver(BaseSolver):
    dbitMapRank = [0x0000, 0x0000, 0x0001, 0x0002, 0x0004, 0x0008, 0x0010, 0x0020, 0x0040, 0x0080, 0x0100, 0x0200, 0x0400, 0x0800, 0x1000, 0x2000]
    dcardRank = ["x", "x", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]

    def __init__(self):
        pass

    @staticmethod
    def get_trump_index(short_name):
        return DDLeadSolver.trump_index_dict[short_name]

    @staticmethod
    def get_player_index(name):
        return DDLeadSolver.name_index_dict[name]

    @staticmethod
    def get_card_pointer(rank):
        pointers = [0x0004, 0x0008, 0x0010, 0x0020, 0x0040, 0x0080, 0x0100, 0x0200, 0x0400, 0x0800, 0x1000, 0x2000, 0x4000]
        return pointers[rank - 1]

    @staticmethod
    def get_hand_suit_value(hand, suit_short_name):
        cards = [v for k, v in hand.items() if k.short_name == suit_short_name][0]
        pointers = [DDLeadSolver.get_card_pointer(card.value.rank) for card in cards if not card.played]
        if len(pointers) == 0:
            return None
        else:
            return sum(pointers)

    @staticmethod
    def get_player_hand(deck, player):
        hand = getattr(deck, player)

        result = []
        result.append(DDLeadSolver.get_hand_suit_value(hand, "S"))
        result.append(DDLeadSolver.get_hand_suit_value(hand, "H"))
        result.append(DDLeadSolver.get_hand_suit_value(hand, "D"))
        result.append(DDLeadSolver.get_hand_suit_value(hand, "C"))

        return result

    @staticmethod
    def prepare_holdings(deck):
        hands = {}
        for player in DDLeadSolver.player_seats:
            hands[player] = DDLeadSolver.get_player_hand(deck, player)

        holdings = []
        for suit in range(4):
            suit_pointers = []
            for player in DDLeadSolver.player_seats:
                suit_pointers.append(hands[player][suit])
            holdings.append(suit_pointers)

        return holdings

    @staticmethod
    def equals_to_string(equals, res):
        p = 0
        m = equals >> 2
        for i in range(15, 1, -1):
            if m & int(DDLeadSolver.dbitMapRank[i]):
                res[p] = bytes(DDLeadSolver.dcardRank[i], "ascii")
                p = p + 1
        res[p] = 0

    @staticmethod
    def prepare_results(fut, title=None, is_print=True):
        if is_print:
            print("{}\n".format(title))
            print("{:6s} {:<6s} {:<6s} {:<6s} {:<6s}".format("card", "suit", "rank", "equals", "score"))

        score_table = {}
        for i in range(fut.contents.cards):
            res = ctypes.create_string_buffer(15)

            score = fut.contents.score[i]
            suit = [suit for suit, rank in DDLeadSolver.trump_index_dict.items() if rank == fut.contents.suit[i]][0]
            card = DDLeadSolver.dcardRank[fut.contents.rank[i]]

            DDLeadSolver.equals_to_string(fut.contents.equals[i], res)
            if is_print:
                print("{:6} {:<6s} {:<6s} {:<6s} {:<6}".format(i, suit, card, res.value.decode("utf-8"), score))

            if score not in score_table.keys():
                score_table[score] = []

            score_table[score].append((suit, card))

            for eqv in res.value.decode("utf-8"):
                score_table[score].append((suit, eqv))

        return score_table

    @staticmethod
    def run_solver(trump, first_player, holdings):
        dl = dds.deal()
        fut3 = dds.futureTricks()

        threadIndex = 0
        line = ctypes.create_string_buffer(80)

        dds.SetMaxThreads(0)

        dl.trump = trump
        dl.first = first_player

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

    @staticmethod
    def error_check(line, res):
        if res != dds.RETURN_NO_FAULT:
            dds.ErrorMessage(res, line)
            print("DDS error: {}".format(line.value.decode("utf-8")))

    @staticmethod
    def score_leads(deck, trump, first):
        trump_index = trump if isinstance(trump, int) else DDLeadSolver.get_trump_index(trump.short)
        first_player_index = first if isinstance(first, int) else DDLeadSolver.get_player_index(first.name)
        holdings = DDLeadSolver.prepare_holdings(deck)

        fut3, line, res = DDLeadSolver.run_solver(trump_index, first_player_index, holdings)
        DDLeadSolver.error_check(line, res)
        score_table = DDLeadSolver.prepare_results(ctypes.pointer(fut3), is_print=False)

        nb_solutions = sum([len(x) for x in list(score_table.values())])
        return score_table, nb_solutions

    @staticmethod
    def best_score(deck, trump, first):
        full_res, __ = DDLeadSolver.score_leads(deck, trump, first)

        return max([k for k in full_res.keys()])

    @staticmethod
    def get_player_best_score_list(deck, player):
        player_index = DDLeadSolver.get_player_index(player)
        first = player_index - 1 if player_index > 0 else 3
        res = []
        for suit in DDLeadSolver.trump_suits:
            res.append(13 - DDLeadSolver.best_score(deck, DDLeadSolver.get_trump_index(suit), first))

        return res

    @staticmethod
    def get_max_tricks_dict(deck):
        max_scores = {}
        for seat in DDLeadSolver.player_seats:
            max_scores[seat] = DDLeadSolver.get_player_best_score_list(deck, seat)

        return max_scores

    @staticmethod
    def get_max_tricks_table(deck):
        max_trick_table = DDLeadSolver.get_max_tricks_dict(deck)

        res = []
        for suit in range(5):
            for player in DDLeadSolver.player_seats:
                res.append(max_trick_table[player][suit])

        assert len(res) == 20, "not enough data"

        return res


class DDParSolver(BaseSolver):
    def __init__(self):
        pass

    @staticmethod
    def get_vul_index(vul):
        if vul["N"] == "NONVUL" and vul["E"] == "NONVUL":
            return 0

        if vul["N"] == "VUL" and vul["E"] == "VUL":
            return 1

        if vul["N"] == "VUL" and vul["E"] == "NONVUL":
            return 2

        if vul["N"] == "NONVUL" and vul["E"] == "VUL":
            return 3

        raise ValueError("Cannot recognise vul")

    @staticmethod
    def show_par_table(table):
        print("{:5} {:<5} {:<5} {:<5} {:<5}".format("", "North", "South", "East", "West"))
        print("{:>5} {:5} {:5} {:5} {:5}".format("NT", table.contents.resTable[4][0], table.contents.resTable[4][2], table.contents.resTable[4][1], table.contents.resTable[4][3]))
        for suit in range(0, dds.DDS_SUITS):
            print(
                "{:>5} {:5} {:5} {:5} {:5}".format(
                    DDParSolver.trump_suits[suit], table.contents.resTable[suit][0], table.contents.resTable[suit][2], table.contents.resTable[suit][1], table.contents.resTable[suit][3]
                )
            )
        print("")

    @staticmethod
    def get_optimal_par_scores(par, is_print=False):
        res = {}
        if is_print:
            print("NS score: {}".format(par.contents.parScore[0].value.decode("utf-8")))
            print("EW score: {}".format(par.contents.parScore[1].value.decode("utf-8")))
            print("NS list : {}".format(par.contents.parContractsString[0].value.decode("utf-8")))
            print("EW list : {}\n".format(par.contents.parContractsString[1].value.decode("utf-8")))

        optimal_score_NS = par.contents.parScore[0].value.decode("utf-8").split(" ")[1]
        
        optimal_contract_str = par.contents.parContractsString[1].value.decode("utf-8").split(":")[1]
        optimal_dealers = optimal_contract_str.split(" ")[0]
        optimal_dealer = None
        if "N" in optimal_dealers:
            optimal_dealer = "N"
        elif "S" in optimal_dealers:
            optimal_dealer = "S"
        elif "E" in optimal_dealers:
            optimal_dealer = "E"
        elif "W" in optimal_dealers:
            optimal_dealer = "W"
        else:
            raise ValueError("Optimal dealer cannot be found")

        optimal_contracts = optimal_contract_str.split(" ")[1]
        import re
        match = re.match(r"([0-9]+)([a-z]+)", optimal_contracts, re.I)
        items = match.groups()

        optimal_level = items[0][0]
        optimal_trump = "NT" if "NT" in items[1][0] else items[1][0]
        is_doubled = "x" if "x" in items[1][0] else ""
        
        res["contract"] = optimal_level + optimal_trump + is_doubled
        res["declarer"] = optimal_dealer
        res["NS_score"] = optimal_score_NS
        return res

    @staticmethod
    def get_par_score(deck, vul, is_print = False):

        score_table = DDLeadSolver.get_max_tricks_table(deck)

        DDtable = dds.ddTableResults()
        pres = dds.parResults()

        line = ctypes.create_string_buffer(80)

        dds.SetMaxThreads(0)

        for suit in range(dds.DDS_STRAINS):
            for pl in range(4):
                ctypes.pointer(DDtable).contents.resTable[suit][pl] = score_table[4 * suit + pl]

        res = dds.Par(ctypes.pointer(DDtable), pres, DDParSolver.get_vul_index(vul))

        if res != dds.RETURN_NO_FAULT:
            dds.ErrorMessage(res, line)
            print("DDS error: {}".format(line.value.decode("utf-8")))

        if is_print:
            DDParSolver.show_par_table(ctypes.pointer(DDtable))
        
        return DDParSolver.get_optimal_par_scores(ctypes.pointer(pres), is_print=is_print)


class DDSolver(DDLeadSolver, DDParSolver):
    def __init__(self):
        pass
