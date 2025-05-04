class Matchup:
    def __init__(self, team1, team2, usesleft):
        self.team1 = team1
        self.team2 = team2
        self.usesleft = usesleft

class Week:
    def __init__(self, name):
        self.name = name
        self.matchups = []
        