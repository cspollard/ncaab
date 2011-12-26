from sys import argv
from crawler import crawl
from teamslist import teamslist
from itertools import permutations
from analyze import *

def main():
    (teamsdict, (homescores, awayscores, neutscores)) = \
            crawl(update=1, bb=0)

    # normalize scores.
    homescores, awayscores, neutscores = norm_venues(homescores,
            awayscores, neutscores)

    # get final scores matrix.
    scores = homescores + awayscores + neutscores
    # scores = (scores > scores.T)

    # games = permutations(["Duke", "North Carolina", "Kentucky", \
            # "Kansas", "Missouri", "Marquette", "Ohio St.", "Indiana",
            # "Louisville"], 2)

    # games = permutations(["Alabama", "Arkansas", "Oklahoma", \
            # "Virginia Tech", "Oklahoma State", "Louisiana State", \
            # "Stanford", "Oregon", "Southern Cal"], 2)
    # print_probs(teamsdict, scores, games)

    # print; print

    valsp = prob_network_ratings(scores)
    valse = energy_min(scores)
    vals = [valsp, valse]

    wins = scores > scores.T
    losses = scores < scores.T

    wl = zip(wins.sum(1), losses.sum(1))

    print_values(teamsdict, teamslist, vals, wl)
    # plot_values(teamsdict, teamslist, vals)


if __name__ == "__main__":
    main()
