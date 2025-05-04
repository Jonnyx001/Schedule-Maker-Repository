class Matchup:
    def __init__(self, hometeam, awayteam, usesleft):
        self.hometeam = hometeam
        self.awayteam = awayteam
        self.usesleft = usesleft

class Week:
    def __init__(self, name):
        self.name = name
        self.matchups = []
        