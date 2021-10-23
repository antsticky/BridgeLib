#! /usr/bin/python

import examples.dds as dds
import examples.hands as hands
import examples.functions as functions
import ctypes

dl = dds.deal()
fut2 = dds.futureTricks()
fut3 = dds.futureTricks()

threadIndex = 0
line = ctypes.create_string_buffer(80)

dds.SetMaxThreads(0)

for handno in range(1):
    dl.trump = hands.trump[handno]
    dl.first = hands.first[handno]

    dl.currentTrickSuit[0] = 0
    dl.currentTrickSuit[1] = 0
    dl.currentTrickSuit[2] = 0

    dl.currentTrickRank[0] = 0
    dl.currentTrickRank[1] = 0
    dl.currentTrickRank[2] = 0

    for h in range(dds.DDS_HANDS):
        for s in range(dds.DDS_SUITS):
            if hands.holdings[handno][s][h] is not None:
                dl.remainCards[h][s] = hands.holdings[handno][s][h]

    target = -1  # No target; find all results
    solutions = 3  # Return all solutions
    mode = 0  # The way dds internally handles the last trick
    res = dds.SolveBoard(dl, target, solutions, mode,
                         ctypes.pointer(fut3), threadIndex)

    if res != dds.RETURN_NO_FAULT:
        dds.ErrorMessage(res, line)
        print("DDS error: {}".format(line.value.decode("utf-8")))

    # match3 = functions.CompareFut(ctypes.pointer(fut3), handno, solutions)

    solutions = 2  # Return only the optmial solutions
    res = dds.SolveBoard(dl, target, solutions, mode,
                         ctypes.pointer(fut2), threadIndex)

    functions.PrintHand(line, dl.remainCards)

    line = "solutions == 3"
    score_table = functions.PrintFut(
        line, ctypes.pointer(fut3), is_print=True)

    nb_solutions = sum([len(x) for x in list(score_table.values())])
    print(f"number of solutions {nb_solutions}")
