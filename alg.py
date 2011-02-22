# alg class
from team import team
from game import game
from math import exp
import random
from datetime import datetime

debug = True
alpha = .001

class alg:
    def __init__(self, teams, games):
        self._teams = teams
        self._games = games

    def randomize(self):
        random.seed()
        for t in self._teams.itervalues():
            t.set_value(2*random.random() - 1)

    def loop(self, nloops):
        i = 0
        games = list(self._games.values())
        n = datetime.now()
        while i < nloops:
            i += 1
            g = random.choice(games)
            decay = self.decay((n - g.date()).days)

            for t in g.teams():
                v1 = t.value()
                v2 = t.opponent(g).value()
                p1 = g.score(t)
                p2 = g.score(t.opponent(g))

                v = t.add_value(decay*self.grad(v1,v2,p1,p2)*alpha)
                if debug:
                    print "adding to", t.name() + ":", v*alpha
                    print "value:", t.value()

        self.normalize()

    def loopold(self):
        n = datetime.now()
        for t in self._teams.itervalues():
            v = 0.0
            games = t.games()
            for g in games:
                sratio = g.score_ratio(t)
                vratio = self.val_ratio(t, g)
                """
                timediff = (datetime.now() - g.date()).days
                if timediff < 28:
                    t.games().remove(g)
                    continue
                """
                decay = self.decay((n - g.date()).days)

                v += decay*(sratio - vratio)

            t.add_value(v*alpha)
            if debug:
                print "adding to", t.name() + ":", v*alpha
                print "value:", t.value()

            # t._update()

        self.normalize()

    def normalize(self):
        max = 0.0
        for t in self._teams.itervalues():
            if t.value() > max:
                max = t.value()

        for t in self._teams.itervalues():
            t.set_value(t.value() / max)

        return

    def grad(self, v1, v2, p1, p2):
        return (v1/v2 - p1/p2)/v2 - (v2/v1 - p2/p1)*v2/(v1*v1) 

    def val_ratio(self, t, g):
        return t.value() / t.opponent(g).value()

    def decay(self, t):
        return exp(-t/128.0)

    def teams(self):
        return self._teams

    def games(self):
        return self._games
