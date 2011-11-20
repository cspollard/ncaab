# analyzes data coming from the crawler.
from sys import argv
from crawler import crawl
from numpy import diag
from scipy.linalg import expm3, expm2
from teamslist import teamslist

def main():
    (teamsdict, (homescores, awayscores, neutscores)) = crawl(filename=argv[1])

    # normalize scores.
    homenorm = homescores.sum()/(homescores != 0).sum()
    awaynorm = awayscores.sum()/(awayscores != 0).sum()
    neutnorm = neutscores.sum()/(neutscores != 0).sum()

    homescores /= homenorm
    awayscores /= awaynorm
    neutscores /= neutnorm

    scores = homescores + awayscores + neutscores

    sym = (scores + scores.T) / 2
    # asym = (scores - scores.T) / 2
    normed = scores/(2*sym + (sym == 0))
    # ratio = scores/(scores.T + (scores.T == 0))
    exped = expm2(normed)
    exped -= diag(diag(exped))
    probs = exped/((exped + exped.T) + (exped == 0))
    probs = probs.sum(axis=1)
    probs /= (exped != 0).sum(axis=1) - 1

    teamval = []
    for team, n in teamsdict.items():
        teamval.append([team, probs[n]])

    teamval = sorted(teamval, key=lambda t: -t[1])

    norm = teamval[0][1]
    for team in teamval:
        print team[0].rjust(30), "%2f" % (team[1]/norm)

if __name__ == "__main__":
    main()
