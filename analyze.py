# analyzes data coming from the crawler.
from numpy import diag, abs as nabs, dot
from scipy.linalg import expm3, expm2, svd

def print_values(teamsdict, vals):

    teamval = []
    for team, n in teamsdict.items():
        teamval.append([team, vals[n]])

    teamval = sorted(teamval, key=lambda t: -t[1])

    for i in xrange(len(teamval)):
        print (teamval[i][0] + " %03d" % (i+1)).rjust(30), "%2f" % (teamval[i][1])


def print_probs(teamsdict, scores, games):
    probs = prob_network(scores)
    for g in games:
        print g[0].rjust(30) + ' : ' + g[1].ljust(30), probs[teamsdict[g[0]],teamsdict[g[1]]]


def prob_network(scores):
    # get known score fractions.
    normed = scores/((scores + scores.T) + (scores == 0))
    exped = expm3(normed, 20)

    # get rid of diagonal part.
    exped -= diag(diag(exped))

    # divide by symmetric part.
    return exped/((exped + exped.T) + (exped == 0) + (exped.T == 0))


def prob_network_ratings(scores):
    probs = prob_network(scores) 
    sums = (probs != 0).sum(axis=1)
    sums += (sums == 0)
    probs = probs.sum(axis=1)
    probs /= sums

    return probs


def energy_min(scores):
    # get known score fractions.
    normed = scores/((scores + scores.T) + (scores == 0))

    M = diag((normed*normed).sum(axis=0)) - (normed*normed.T)

    return nabs(svd(M)[-1][-1])


def norm_venues(homescores, awayscores, neutscores):
    homenorm = homescores.sum()/(homescores != 0).sum()
    awaynorm = awayscores.sum()/(awayscores != 0).sum()
    neutnorm = neutscores.sum()/(neutscores != 0).sum()

    print "each home point is worth %4f points" % (1/homenorm)
    print "each away point is worth %4f points" % (1/awaynorm)
    print "each neutral point is worth %4f points" % (1/neutnorm)

    homescores /= homenorm
    awayscores /= awaynorm
    neutscores /= neutnorm

    return homescores, awayscores, neutscores
