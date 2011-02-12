# alg class
from team import team
from game import game
from math import exp
import random
from datetime import datetime

debug = False

class alg:
    def __init__(self, teams, games):
        self._teams = teams
        self._games = games

    def randomize(self):
        random.seed()
        for t in self._teams.itervalues():
            t.set_value(2*random.random() - 1)

    def loop(self):
        for t in self._teams.itervalues():
            games = t.games()
            val = 0.0
            for g in games:
                diff = g.score_diff(t)
                val += self.val_diff(t, g)

            val /= t.ngames()

            t.set_value(val)
            if debug:
                print "setting", t.name() + ":", val

    def val_diff(self, t, g):
        oppval = t.opponent(g).value()
        score_diff = g.score_diff(t)
        return (self.curve(score_diff) + oppval) * \
            self.decay((datetime.now() - g.date()).days)

    def curve(self, val):
        val = val/50.0
        return (exp(val)-exp(-val))/(exp(val)+exp(-val))

    def decay(self, t):
        return exp(-t/120.0)

    def teams(self):
        return self._teams

    def games(self):
        return self._games
