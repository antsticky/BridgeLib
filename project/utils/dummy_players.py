from project.base.people import Player, Team

def define_players():
    RR = Team("RR", 666)

    Simon = Player("Simon", "Pop Simon", team=RR)
    Odon = Player("Ödön", "Tök Ödön", team=RR)

    Andi = Player("Andi", "Sinkovicz Andrea", team=RR)
    Peter = Player("Peter", "Sinkovicz Péter", team=RR)

    return Andi, Peter, Simon, Odon
