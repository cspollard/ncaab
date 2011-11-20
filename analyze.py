# analyzes data coming from the crawler.
from sys import argv
from crawler import crawl
from numpy import diag, abs as nabs, dot, nan_to_num
from scipy.linalg import expm3, expm2, svd
from teamslist import teamslist

def main():
    (teamsdict, (homescores, awayscores, neutscores)) = \
            crawl(filename=argv[1], update=0)

    # normalize scores.
    # homescores, awayscores, neutscores = norm_venues(homescores,
            # awayscores, neutscores)

    # get final scores matrix.
    scores = homescores + awayscores + neutscores
    scores = (scores > scores.T)

    vals = prob_network(scores)
    # vals = energy_min(scores)

    teamval = []
    for team, n in teamsdict.items():
        teamval.append([team, vals[n]])

    teamval = sorted(teamval, key=lambda t: -t[1])

    for i in xrange(len(teamval)):
        print (teamval[i][0] + " %03d" % (i+1)).rjust(30), "%2f" % (teamval[i][1])


def prob_network(scores):
    # get known score fractions.
    normed = scores/((scores + scores.T) + (scores == 0))
    exped = expm3(normed, 20)

    # get rid of diagonal part.
    exped -= diag(diag(exped))

    # divide by symmetric part.
    probs = exped/((exped + exped.T) + (exped == 0))
    probs = probs.sum(axis=1)
    sums = (exped != 0).sum(axis=1)
    sums += (sums == 0)
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

    homescores /= homenorm
    awayscores /= awaynorm
    neutscores /= neutnorm

    return homescores, awayscores, neutscores


if __name__ == "__main__":
    main()
