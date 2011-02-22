# alg class
from team import team
from game import game
from math import exp
import random
from datetime import datetime

debug = True

class alg:
    def __init__(self, teams, games):
        random.seed()
        self._teams = teams
        self._games = games

    def randomize(self):
        random.seed()
        for t in self._teams.itervalues():
            t.set_value(2*random.random() - 1)

    def loop(self, nloops=1000000, alpha=.03):
        i = 0
        games = list(self._games.values())
        n = datetime.now()

        while i < nloops:
            i += 1
            g = random.choice(games)
            decay = self.decay((n - g.date()).days)

            (t1, t2) = g.teams()
            v1 = t1.value()
            v2 = t2.value()
            (p1, p2) = g.scores()

            v = decay*self.grad(v1,v2,p1,p2)*alpha
            t1.add_value(v*alpha)
            t2.add_value(-v*alpha)
            if debug:
                print "adding to", t1.name() + ":", v*alpha
                print "value:", t1.value()
                print "adding to", t2.name() + ":", -v*alpha
                print "value:", t2.value()


    def normalize(self):
        max = 0.0
        for t in self._teams.itervalues():
            if t.value() > max:
                max = t.value()

        for t in self._teams.itervalues():
            t.set_value(t.value() / max)

        return

    def grad(self, v1, v2, p1, p2):
        return (v2/v1 - p2/p1)*v2/v1 - (v1/v2 - p1/p2)*v1/v2 

    def decay(self, t):
        return exp(-t/128.0)

    def teams(self):
        return self._teams

    def games(self):
        return self._games
