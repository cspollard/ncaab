# game class.
from team import team
from hashlib import new as newhash

class game:
    def __init__(self, date, teams, scores, home):
        self._idx = newhash(str(date) + str(team[0]) +
                str(team[1])).hexdigest()
        self._date = date
        self._teams = teams
        self._scores = scores
        self._home = home

        if home == 0:
            self._away = 1
        elif home == 1:
            self._away = 0
        else:
            self._home = -1
            self._away = -1

        if scores[0] > scores[1]:
            self._winner = 0
            self._loser = 1
        else:
            self._winner = 1
            self._loser = 0

    def __eq__(self, g):
        return self.idx() == g.idx()

    def idx(self):
        return self._idx

    def date(self):
        return self._date

    def teams(self):
        return self._teams

    def winner(self):
        return self._teams[self._winner]
    
    def loser(self):
        return self._teams[self._loser]

    def scores(self):
        return self._scores

    def winner_score(self):
        return self._scores[self._winner]

    def loser_score(self):
        return self._scores[self._loser]

    def score_diff(self):
        return self._scores[self._winner] - self._scores[self._loser]

    def home_team(self):
        if self._home == -1:
            return None
        else:
            return self._teams[self._home]

    def away_team(self):
        if self._away == -1:
            return None
        else:
            return self._teams[self._away]

