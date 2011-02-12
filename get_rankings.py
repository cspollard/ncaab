from crawler import crawler
from alg import alg
from sys import argv, stdout

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
a = alg(c.teams(), c.games())
a.randomize()

for i in xrange(100):
    a.loop()

teams = a.teams().values()
teams.sort(cmp=tcmp)
teams.reverse()

print
print

for t in teams:
    print "%20s\t%02d-%02d\t%+6f" % (t.name()[:20], t.nwins(), \
            t.nlosses(), t.value())

print
print

for t in teams:
    print "%20s\t%02d-%02d\t%+6f" % (t.name()[:20], t.nwins(), \
            t.nlosses(), t.value())

    games = t.games()
    games.sort(cmp=gcmp)
    sos = 0

    for g in games:
        opp = t.opponent(g)
        print "\t%03d-%03d\t%20s (%+6f)\t%+6f" % (g.score(t), g.score(opp), \
                opp.name()[:20], opp.value(), a.val_diff(t, g))
        sos += opp.value()

    print "\t\tSOS: %+6f" % (sos/t.ngames())

    print
    print
