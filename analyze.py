# analyzes data coming from the crawler.
from crawler import crawl
from scipy.linalg import det, block_diag, expm

(teamsdict, (homescores, awayscores, neutscores)) = crawl()

# normalize scores.
# homenorm = homescores.sum()/(homescores != 0).sum()
# awaynorm = awayscores.sum()/(awayscores != 0).sum()
# neutnorm = neutscores.sum()/(neutscores != 0).sum()

# homescores /= homenorm
# awayscores /= awaynorm
# neutscores /= neutnorm

scores = homescores + awayscores + neutscores

sym = (scores + scores.T) / 2
asym = (scores - scores.T) / 2
normed = scores/(2*sym + (sym == 0))
print block_diag(scores)
print det(scores)
print det(sym)
print det(asym)
print det(normed)
exped = expm(normed, 15)
print det(exped)

for team1 in teamsdict:
        print team1, exped[teamsdict[team1], teamsdict[team1]]

"""
        if neutscores[teamsdict[team1], teamsdict[team2]]:
            print team1, neutscores[teamsdict[team1], \
                    teamsdict[team2]], team2, \
                    neutscores[teamsdict[team2], teamsdict[team1]], "N"

        if homescores[teamsdict[team1], teamsdict[team2]]:
            print team1, homescores[teamsdict[team1], \
                    teamsdict[team2]], team2, \
                    awayscores[teamsdict[team2], teamsdict[team1]]
"""
