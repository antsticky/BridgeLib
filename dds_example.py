from project.base.board import Board
from project.analytics.dds import DDSolver
from project.base.people import Team, Player

from project.base.board import Deck


def define_players():
    RR = Team("RR", 666)

    Zsuzsa = Player("Zsuzsa", "Réti Zsuzsa", team=RR)
    Gyorgy = Player("Gyorgy", "Ferenci Gyorgy", team=RR)

    Andi = Player("Andi", "Sinkovicz Andrea", team=RR)
    Peter = Player("Peter", "Sinkovicz Péter", team=RR)

    return Andi, Peter, Zsuzsa, Gyorgy


def do_bid(board, is_show=True):
    board.bid("1H", "W")
    board.bid("x", "N")
    board.bid("2H", "E")
    board.bid("2NT", "S")

    board.bid("p", "W")
    board.bid("p", "N")
    board.bid("p", "E")

    if is_show:
        board.bids.show()


def do_play(board, is_show=True, show_played=True):
    board.play("H5", "W")
    board.play("HT", "N")
    board.play("HJ", "E")
    board.play("HA", "S")

    board.play("S5", "S")
    board.play("ST", "W")
    board.play("S2", "N")
    board.play("S3", "E")

    board.play("H4", "W")
    board.play("HK", "N")
    board.play("H8", "E")
    board.play("H2", "S")

    board.play("S7", "N")
    board.play("S4", "E")
    board.play("SK", "S")
    board.play("SJ", "W")

    board.play("S9", "S")
    board.play("SQ", "W")
    board.play("SA", "N")
    board.play("S6", "E")

    board.play("S8", "N")
    board.play("C5", "E")
    board.play("D3", "S")
    board.play("D2", "W")

    board.play("DK", "N")
    board.play("DA", "E")
    board.play("D4", "S")
    board.play("C9", "W")

    board.play("H7", "E")
    board.play("D5", "S")
    board.play("HQ", "W")
    board.play("D6", "N")

    board.play("H9", "W")
    board.play("C2", "N")
    board.play("C7", "E")
    board.play("C4", "S")

    board.play("H6", "W")
    board.play("C3", "N")
    board.play("CJ", "E")
    board.play("C6", "S")

    board.play("H3", "W")
    board.play("D9", "N")
    board.play("D8", "E")
    board.play("C8", "S")

    board.play("CK", "W")
    board.play("CT", "N")
    board.play("DT", "E")
    board.play("CA", "S")

    board.play("D7", "S")
    board.play("CQ", "W")
    board.play("DQ", "N")
    board.play("DJ", "E")

    if is_show:
        board.deck.show(show_played=show_played)


if __name__ == "__main__":
    N_player, S_player, E_player, W_player = define_players()

    cum_sum_point = 0
    your_cum_sum_point = 0
    for i in range(20):
        board1 = Board(board_nb=i + 1)
        board1.seating(N=N_player, S=S_player, E=E_player, W=W_player)
        board1.load_deck(file_name="misc/boards.txt", line_idx=i)

        optimal = DDSolver.get_par_score(deck=board1.deck, vul=board1.is_vul, is_print=False)
        print("=" * 40)
        print(f'{optimal.get("declarer")}: {optimal.get("contract")}\n')

        opener = Deck.show_opener_hand(board1, optimal["declarer"])

        test_lead = input("\nWhat is your opening lead? ")
        print("\n")

        assert len(test_lead) == 2, "Wrong format"

        board1.deck.show()

        trump_suit = "NT" if optimal["contract"][1] == "N" else optimal["contract"][1]
        lead_scores, best_score, _ = DDSolver.score_leads(deck=board1.deck, trump=trump_suit, first=opener)
        lead_score = DDSolver.get_lead_score(lead_scores, test_lead, is_print=True)

        your_cum_sum_point += lead_score
        cum_sum_point += best_score
        print(f"\n\nYour score is {lead_score} out of {best_score}")
        print(f"Your overall score is {your_cum_sum_point}/{cum_sum_point} = {int(100*your_cum_sum_point/cum_sum_point)}%")
        print("=" * 40)

        is_next = input("\nOne more? [y/n] ")

        if is_next != "y":
            break
