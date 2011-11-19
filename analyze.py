# analyzes data coming from the crawler.
from sys import argv
from crawler import crawl
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
    asym = (scores - scores.T) / 2
    normed = scores/(2*sym + (sym == 0))
    exped = expm3(normed, 50)

    teamval = []
    for team in teamsdict:
        teamval.append([team,
            exped[teamsdict[team]][0]/exped[0][teamsdict[team]],
            exped[teamsdict[team]][1]/exped[1][teamsdict[team]],
            exped[teamsdict[team]][2]/exped[2][teamsdict[team]]])

    teamval = sorted(teamval, key=lambda t: -t[1])

    for team in teamval:
        print team[0].rjust(30), "%2f %2f %2f %2f" % (team[1], team[2],
                team[3], team[1]/team[2])

if __name__ == "__main__":
    main()
