from crawler import crawler
from alg import alg
from sys import argv, stdout
from datetime import datetime
from numpy import zeros
from math import sqrt, exp

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

c = crawler(filename=argv[1])
teams = c.teams().values()
games = c.games().values()

l = len(teams)
team_dict = dict(zip(teams, xrange(l)))
scores = zeros((l, l))

n = datetime.now()

home_tot = 0
away_tot = 0
haratios = 0
nhomegames = 0
for g in games:
    if g.home() != -1:
        home_tot += g.score(g.home_team())
        away_tot += g.score(g.away_team())
        haratios += g.score_ratio(g.home_team())
        nhomegames += 1

home_bonus = (home_tot+away_tot)/(2.*home_tot)
away_bonus = (home_tot+away_tot)/(2.*away_tot)
print "home bonus: %4f, away bonus: %4f" % (home_bonus, away_bonus)

for g in games:
    if g.home() == -1:
        t1, t2 = g.teams()
        p1, p2 = g.score(t1), g.score(t2)
    else:
        t1, t2 = g.home_team(), g.away_team()
        p1 = g.score(t1)*home_bonus
        p2 = g.score(t2)*away_bonus

    scores[team_dict[t1]][team_dict[t2]] += p1
    scores[team_dict[t2]][team_dict[t1]] += p2


a = alg(scores)
vec = a.minimize()

map(lambda (t,v): t.set_value(v), zip(teams, vec))

teams.sort(cmp=tcmp)
teams.reverse()


rank = 0
for t in teams:
    rank += 1
    print "%3d) %20s\t\t%02d-%02d\t\t%+6f" % (rank, t.name()[:20], t.nwins(), \
            t.nlosses(), t.value())

print "\t\t\tEnergy = %+6f" % (a.E())
stdout.flush()

for t in teams:
    print
    print

    print "%20s\t%02d-%02d\t%+6f" % (t.name()[:20], t.nwins(), \
            t.nlosses(), t.value())

    gs = t.games()
    gs.sort(cmp=gcmp)

    sos = 0
    for g in gs:
        if g not in games:
            continue
        opp = t.opponent(g)
        if opp not in teams:
            continue
        print "\t%03d-%03d\t%20s %s (%+6f)\t%+6f" % (g.score(t), g.score(opp), \
                opp.name()[:20], {None: 'N', t: 'H', opp: 'A'}[g.home_team()], \
                opp.value(), a.contribution(team_dict[t], team_dict[t.opponent(g)]))

        sos += opp.value()

    print "\t\tSOS: %+6f" % (sos/t.ngames())
