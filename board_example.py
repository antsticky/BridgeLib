from project.base.board import Board
from project.base.people import Team, Player


# TODO: eliminated mutable default variables eg. mylist = []
# TODO: activate claim functionality
# TODO: improve analytics
# TODO: implement open lead checker
# TODO: develop tournament functionality


def define_players():
    RR = Team("RR", 666)

    Zsuzsa = Player("Zsuzsa", "Réti Zsuzsa", team=RR)
    Gyorgy = Player("Gyorgy", "Ferenci Gyorgy", team=RR)

    Andi = Player("Andi", "Sinkovicz Andrea", team=RR)
    Peter = Player("Peter", "Sinkovicz Péter", team=RR)

    return Zsuzsa, Gyorgy, Andi, Peter


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
    Zsuzsa, Gyorgy, Andi, Peter = define_players()

    board1 = Board(board_nb=1, dealer="W")
    board1.seating(N=Andi, S=Peter, E=Zsuzsa, W=Gyorgy)

    # ------ Deal ------
    # board1.deal()
    # board1.deck.sort()
    board1.load_deck(file_name="misc/boards.txt", line_idx=2)
    # board1.deck.save(file_name="misc/boards.txt",write_type="a")

    # ------ Bid  ------
    do_bid(board=board1)

    # ------ Play ------
    do_play(board=board1)

    print(board1.contract, board1.contract.value())
