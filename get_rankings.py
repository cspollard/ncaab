from crawler import crawler
from alg import alg
from sys import argv, stdout
import datetime
from numpy import zeros
from math import sqrt

def tcmp(t1, t2):
    if t1.value() > t2.value():
        return 1
    elif t1.value() < t2.value():
        return -1
    else:
        return 0

def gcmp(g1, g2):
    if g1.date() > g2.date():
        return 1
    elif g1.date() < g2.date():
        return -1
    else:
        return 0

c = crawler(argv[1])
teams = c.teams().values()
games = c.games().values()
l = len(teams)
scores = zeros((l, l))

team_dict = dict(zip(teams, xrange(l)))

for g in games:
    t1, t2 = g.teams()
    p1, p2 = g.score(t1), g.score(t2)
    scores[team_dict[t1]][team_dict[t2]] += p1
    scores[team_dict[t2]][team_dict[t1]] += p2

a = alg(scores)
vec = a.minimize()

map(lambda (t,v): t.set_value(v), zip(teams, vec))

teams.sort(cmp=tcmp)
teams.reverse()

for t in teams:
    print "%20s\t%02d-%02d\t%+6f\t%+6f" % (t.name()[:20], t.nwins(), \
            t.nlosses(), t.value(), t.value()/teams[0].value())

"""
print
print

n = datetime.datetime.now()

for t in teams:
    print "%20s\t%02d-%02d\t%+6f" % (t.name()[:20], t.nwins(), \
            t.nlosses(), t.value())

    games = t.games()
    games.sort(cmp=gcmp)
    sos = 0
    mu = 0
    sigma = 0

    for g in games:
        # x = (g.score_ratio(t) - a.val_ratio(t,g)) * \
                # a.decay((n - g.date()).days)/t.opponent(g).value()

        opp = t.opponent(g)
        print "\t%03d-%03d\t%20s (%+6f)" % (g.score(t), g.score(opp), \
                opp.name()[:20], opp.value())

        sos += opp.value()
        # mu += x
        # sigma += x*x

    print "\t\tSOS: %+6f" % (sos/t.ngames())

    print
    print

    """
