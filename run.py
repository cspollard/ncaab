from sys import argv
from crawler import crawl
from teamslist import teamslist
from itertools import permutations
from analyze import *

def main():
    (teamsdict, (homescores, awayscores, neutscores)) = \
            crawl(update=0, bb=1)

    # normalize scores.
    homescores, awayscores, neutscores = norm_venues(homescores,
            awayscores, neutscores)

    # get final scores matrix.
    scores = homescores + awayscores + neutscores
    # scores = (scores > scores.T)

    # games = permutations(["Duke", "North Carolina", "Kentucky", \
            # "Kansas", "Missouri", "Marquette", "Ohio St."], 2)

    # games = permutations(["Alabama", "Arkansas", "Oklahoma", \
            # "Virginia Tech", "Oklahoma State", "Louisiana State", \
            # "Stanford", "Oregon", "Southern Cal"], 2)
    # print_probs(teamsdict, scores, games)

    # print; print

    vals = prob_network_ratings(scores)
    # vals = energy_min(scores)

    print_values(teamsdict, vals)


if __name__ == "__main__":
    main()
