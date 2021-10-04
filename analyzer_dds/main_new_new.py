from bridgeLib.people import Team, Player
from bridgeLib.board import Board

if __name__ == "__main__":
    RR = Team("RR", 666)

    Zsuzsa = Player("Zsuzsa", "Réti Zsuzsa", team=RR)
    Gyorgy = Player("Gyorgy", "Ferenci Gyorgy", team=RR)

    Andi = Player("Andi", "Sinkovicz Andrea", team=RR)
    Peter = Player("Peter", "Sinkovicz Péter", team=RR)

    board1 = Board(1)
    board1.seating(N=Andi, S=Peter, E=Zsuzsa, W=Gyorgy)
    board1.deal()

    board1.deck.sort()
    board1.deck.show()

    #board1.load()