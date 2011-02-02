# alg class
from team import team
from game import game
from math import exp
import random
from datetime import datetime

class alg:
    def __init__(self, teams, games):
        self._teams = teams
        self._games = games


    def loop(self):
        for t in self._teams.itervalues():
            games = t.games()
            val = 0.0
            for g in games:
                diff = g.score_diff(t)
                val += self.val_diff(t, g)

            val /= t.ngames()

            t.set_value(val)

    def val_diff(self, t, g):
        oppval = t.opponent(g).value()
        score_diff = g.score_diff(t)
        pm = {False: -1, True: 1}[score_diff > 0]
        return self.curve((1 + pm*oppval) * score_diff) * \
                self.decay((datetime.now() - g.date()).days)

    def curve(self, val):
        # val = val/10.0
        return (exp(val)-exp(-val))/(exp(val)+exp(-val))

    def decay(self, t):
        return exp(-t/64.0)

    def teams(self):
        return self._teams

    def games(self):
        return self._games
