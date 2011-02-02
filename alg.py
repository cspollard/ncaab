# alg class
from team import team
from game import game
from math import exp
import random

class alg:
    def __init__(self, teams, games):
        self._teams = teams
        self._games = games


    def loop(self):
        for t in self._teams.itervalues():
            games = t.games()
            val = 0.0
            for g in games:
                val += self.curve((1+t.opponent(g).value()) *
                        g.score_diff(t))
            val /= t.ngames()

            t.set_value(val)

    def curve(self, val):
        val = val/10
        return (exp(val)-exp(-val))/(exp(val)+exp(-val))

    def decay(self, val):
        return exp(-val)

    def day_diff(self, d1, d2):
        return (d1-d2)/86400000000

    def teams(self):
        return self._teams

    def games(self):
        return self._games
