from crawler import crawler
from alg import alg
from sys import argv, stdout
from datetime import datetime
from numpy import zeros
from math import sqrt, exp
from team import team

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

def make_list(n, m):
    l = []
    for i in xrange(n):
        l.append([])
        for j in xrange(m):
            l[i].append([])

    return l


c = crawler(filename=argv[1])
teams = c.teams().values()
games = c.games().values()

l = len(teams)
team_dict = dict(zip(teams, xrange(l)))
scores = make_list(l, l)

n = datetime.now()

home_tot = 0.
away_tot = 0.
neut_tot = 0.
nhome = 0.
nneut = 0.
for g in games:
    if g.home() != -1:
        home_tot += g.score(g.home_team())
        away_tot += g.score(g.away_team())
        nhome += 1
    else:
        neut_tot += sum(map(g.score, g.teams()))
        nneut += 2

naway = nhome

home_bonus = nhome/(nhome+naway+nneut) * \
        (home_tot+away_tot+neut_tot)/home_tot

away_bonus = naway/(nhome+naway+nneut) * \
        (home_tot+away_tot+neut_tot)/away_tot

neut_bonus = nneut/(nhome+naway+nneut) * \
        (home_tot+away_tot+neut_tot)/neut_tot

print "home : %4f, home pts: %5f, home ppg: %3f" % (nhome,
        home_tot, home_tot/nhome)
print "away : %4f, away pts: %5f, away ppg: %3f" % (naway,
        away_tot, away_tot/naway)
print "neut : %4f, neut pts: %5f, neut ppg: %3f" % (nneut,
        neut_tot, neut_tot/nneut)
print "home bonus: %4f, away bonus: %4f, neut bonus: %4f" % \
    (home_bonus, away_bonus, neut_bonus)

for g in games:
    if g.home() == -1:
        t1, t2 = g.teams()
        p1, p2 = g.score(t1)*neut_bonus, g.score(t2)*neut_bonus
    else:
        t1, t2 = g.home_team(), g.away_team()
        p1 = g.score(t1)*home_bonus
        p2 = g.score(t2)*away_bonus

    scores[team_dict[t1]][team_dict[t2]].append(p1)
    scores[team_dict[t2]][team_dict[t1]].append(p2)

a = alg(scores)
vec = a.minimize()

map(lambda (t,v): t.set_value(v), zip(teams, vec))

teams.sort(cmp=tcmp)
teams.reverse()

rank = 0
for t in teams:
    rank += 1
    print "%3d) %25s\t%02d-%02d\t%+6f" % (rank, t.name()[:25], t.nwins(), \
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
    print "\t\tconts: %+6f" % a.conts[team_dict[t]][team_dict[t]]
