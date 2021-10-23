import examples.dds as dds
# TODO: eliminate this dependency
import examples.functions as functions
import ctypes

SPADES = 0
HEARTS = 1
DIAMONDS = 2
CLUBS = 3
NOTRUMP = 4

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

R2 = 0x0004
R3 = 0x0008
R4 = 0x0010
R5 = 0x0020
R6 = 0x0040
R7 = 0x0080
R8 = 0x0100
R9 = 0x0200
RT = 0x0400
RJ = 0x0800
RQ = 0x1000
RK = 0x2000
RA = 0x4000

holdings = [
    [sum([RQ, RJ, R3]), R9 | R8 |
     R6 | R4, RK | RT | R2,  RA | R7 | R5],
    [RT | R4, RQ | RJ | R6 | R2, RK | R7 | R5, RA | R9 | R8 | R3],
    [RK | RQ | RJ | R9 | R6 | R5 | R2, None, RA | R8 | R7 | R4, RT | R3],
    [RK, RA | R8 | R7 | R6 | R2, RJ | R5 | R3, RQ | RT | R9 | R4]
]

# // Useful constants
dbitMapRank = [
    0x0000, 0x0000, 0x0001, 0x0002, 0x0004, 0x0008, 0x0010, 0x0020,
    0x0040, 0x0080, 0x0100, 0x0200, 0x0400, 0x0800, 0x1000, 0x2000
]

dcardRank = [
    'x', 'x', '2', '3', '4', '5', '6', '7',
    '8', '9', 'T', 'J', 'Q', 'K', 'A'
]

dcardSuit = ["S", "H", "D", "C", "N"]
dcardHand = ['N' 'E', 'S', 'W']


def equals_to_string(equals, res):
    p = 0
    m = equals >> 2
    for i in range(15, 1, -1):
        if m & int(dbitMapRank[i]):
            res[p] = bytes(dcardRank[i], "ascii")
            p = p + 1
    res[p] = 0


def PrintFut(fut, title=None, is_print=True):
    if is_print:
        print("{}\n".format(title))
        print("{:6s} {:<6s} {:<6s} {:<6s} {:<6s}".format(
            "card", "suit", "rank", "equals", "score"))

    score_table = {}
    for i in range(fut.contents.cards):
        res = ctypes.create_string_buffer(15)

        score = fut.contents.score[i]
        suit = dcardSuit[fut.contents.suit[i]]
        card = dcardRank[fut.contents.rank[i]]

        equals_to_string(fut.contents.equals[i], res)
        if is_print:
            print("{:6} {:<6s} {:<6s} {:<6s} {:<6}".format(
                i,
                suit,
                card,
                res.value.decode("utf-8"),
                score))

        if score not in score_table.keys():
            score_table[score] = []

        score_table[score].append((suit, card))

        for eqv in res.value.decode("utf-8"):
            score_table[score].append((suit, eqv))

        pass
    print()
    return score_table


def solver(trump, first, holdings):
    dl = dds.deal()
    fut3 = dds.futureTricks()

    threadIndex = 0
    line = ctypes.create_string_buffer(80)

    dds.SetMaxThreads(0)

    dl.trump = trump
    dl.first = first

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
    res = dds.SolveBoard(dl, target, solutions, mode,
                         ctypes.pointer(fut3), threadIndex)

    if res != dds.RETURN_NO_FAULT:
        dds.ErrorMessage(res, line)
        print("DDS error: {}".format(line.value.decode("utf-8")))

    # TODO: delete this
    functions.PrintHand(line, dl.remainCards)

    score_table = PrintFut(
        ctypes.pointer(fut3), is_print=False)

    nb_solutions = sum([len(x) for x in list(score_table.values())])

    return score_table, nb_solutions


if __name__ == "__main__":
    trump = NOTRUMP
    first = WEST

    score_table, _ = solver(trump, first, holdings)
    print(score_table)
