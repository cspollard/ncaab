# analyzes data coming from the crawler.
from sys import argv
from crawler import crawl
from numpy import diag, abs as nabs, dot
from scipy.linalg import expm3, expm2, svd
from teamslist import teamslist

def main():
    (teamsdict, (homescores, awayscores, neutscores)) = crawl(filename=argv[1])

    # normalize scores.
    # homescores, awayscores, neutscores = norm_venues(homescores,
            # awayscores, neutscores)

    # get final scores matrix.
    scores = homescores + awayscores + neutscores

    vals = prob_network(scores)

    print vals

    teamval = []
    for team, n in teamsdict.items():
        teamval.append([team, vals[n]])

    teamval = sorted(teamval, key=lambda t: -t[1])

    for team in teamval:
        print team[0].rjust(30), "%2f" % (team[1])


def prob_network(scores):
    # get known score fractions.
    normed = scores/((scores + scores.T) + (scores == 0))
    exped = expm3(normed, 50)

    print (exped < 0).sum()
    # get rid of diagonal part.
    exped -= diag(diag(exped))

    # divide by symmetric part.
    probs = exped/((exped + exped.T) + (exped == 0))
    print ((exped + exped.T) + (exped == 0) < .001).sum()
    probs = probs.sum(axis=1)
    probs /= (exped != 0).sum(axis=1)

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
