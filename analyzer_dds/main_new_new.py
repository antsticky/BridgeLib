from bridgeLib.people import Team, Player
from bridgeLib.board import Board

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
    board1.deal()
    
    board1.deck.sort()
    board1.deck.show()

    # ------ Bid  ------
    board1.bid("p", "W")
    board1.bid("1NT", "N")
    board1.bid("p", "E")
    board1.bid("2D", "S")

    board1.bid("p", "W")
    board1.bid("2H", "N")
    board1.bid("p", "E")
    board1.bid("6H", "S")

    board1.bid("p", "W")
    board1.bid("p", "N")
    board1.bid("p", "E")

    print(board1.contract)
    board1.bids.show()

    # ------ Play ------

    for seat in ["E", "W", "N", "S"]:
        for suit in ["S", "H", "D", "C"]:
            for rank in ["2", "3", "4", "Q", "K"]:
                board1.play(suit + rank, seat)


    #board1.deck.show(show_played=True)
    #print()
    board1.deck.show(show_played=True)