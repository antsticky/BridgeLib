from project.base.people import Team, Player
from project.base.board import Board

# TODO: eliminated mutable default variables eg. mylist = []

if __name__ == "__main__":
    # ------ DEFINE SETUP ------
    RR = Team("RR", 666)

    Zsuzsa = Player("Zsuzsa", "Réti Zsuzsa", team=RR)
    Gyorgy = Player("Gyorgy", "Ferenci Gyorgy", team=RR)

    Andi = Player("Andi", "Sinkovicz Andrea", team=RR)
    Peter = Player("Peter", "Sinkovicz Péter", team=RR)

    board1 = Board(board_nb=1, dealer="W")

    # ------ Seating ------
    board1.seating(N=Andi, S=Peter, E=Zsuzsa, W=Gyorgy)

    # ------ Deal ------
    # board1.deal()
    # board1.deck.sort()
    # board1.deck.show()
    # board1.deck.save(file_name="misc/boards.txt",write_type="a")

    board1.load_deck(file_name="misc/boards.txt", line_idx=2)
    # board1.deck.show()

    # ------ Bid  ------
    board1.bid("1H", "W")
    board1.bid("x", "N")
    board1.bid("2H", "E")
    board1.bid("2NT", "S")

    board1.bid("p", "W")
    board1.bid("p", "N")
    board1.bid("p", "E")

    board1.bids.show()

    # ------ Play ------
    board1.play("H5", "W")
    board1.play("HT", "N")
    board1.play("HJ", "E")
    board1.play("HA", "S")

    board1.play("S5", "S")
    board1.play("ST", "W")
    board1.play("S2", "N")
    board1.play("S3", "E")

    board1.play("H4", "W")
    board1.play("HK", "N")
    board1.play("H8", "E")
    board1.play("H2", "S")

    board1.play("S7", "N")
    board1.play("S4", "E")
    board1.play("SK", "S")
    board1.play("SJ", "W")

    board1.play("S9", "S")
    board1.play("SQ", "W")
    board1.play("SA", "N")
    board1.play("S6", "E")

    board1.play("S8", "N")
    board1.play("C5", "E")
    board1.play("D3", "S")
    board1.play("D2", "W")

    board1.play("DK", "N")
    board1.play("DA", "E")
    board1.play("D4", "S")
    board1.play("C9", "W")

    board1.play("H7", "E")
    board1.play("D5", "S")
    board1.play("HQ", "W")
    board1.play("D6", "N")

    board1.play("H9", "W")
    board1.play("C2", "N")
    board1.play("C7", "E")
    board1.play("C4", "S")

    board1.play("H6", "W")
    board1.play("C3", "N")
    board1.play("CJ", "E")
    board1.play("C6", "S")

    board1.play("H3", "W")
    board1.play("D9", "N")
    board1.play("D8", "E")
    board1.play("C8", "S")

    board1.play("CK", "W")
    board1.play("CT", "N")
    board1.play("DT", "E")
    board1.play("CA", "S")

    board1.play("D7", "S")
    board1.play("CQ", "W")
    board1.play("DQ", "N")
    board1.play("DJ", "E")

    board1.deck.show(show_played=True)

    print(board1.nb_tricks)

    print(board1.contract, board1.contract.value())
