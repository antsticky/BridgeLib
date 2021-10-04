class Team:
    def __init__(self, name, id=None):
        self.name = name
        self.id = id

    def __eq__(self, other):
        if all([self.name == other.name, self.id == other.id]):
            return True
        else:
            return False


class Player:
    def __init__(self, name, full_name, id=None, team=None):
        self.name = name
        self.full_name = full_name
        self.id = id
        self.team = team


class TablePlayers:
    def __init__(self, N, S, E, W):
        self.N = N
        self.S = S
        self.E = E
        self.W = W

    @property
    def NS_team(self):
        if self.N.team == self.S.team:
            return self.N.team
        else:
            raise ValueError("Players teamname does not match")

    @property
    def EW_team(self):
        if self.E.team == self.W.team:
            return self.E.team
        else:
            raise ValueError("Players teamname does not match")
