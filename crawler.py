# imports ncaabb data from kenpom.com
from subprocess import call
from numpy import zeros, resize
from scipy.sparse import csr_matrix

def crawl(filename=None, url=None, update=0):
    if not filename:
        filename = "cbbga12.txt"
    if not url:
        url = "http://kenpom.com/cbbga12.txt"
    if update:
        call(["rm", filename])
        call(["wget", url])

    f = open(filename)
    games = f.readlines()
    f.close()

    nteams = 0
    teamsdict = {}
    homegames = zeros((500,500))
    awaygames = zeros((500,500))
    neutgames = zeros((500,500))

    for g in games:
        data = g.split()[1:]

        # get the teams and scores from the game.
        i = 1
        while 1:
            try:
                score1 = int(data[i])
                break
            except ValueError:
                i += 1

        team1 = " ".join(data[:i])

        j = i+2
        while 1:
            try:
                score2 = int(data[j])
                break
            except ValueError:
                j += 1

        team2 = " ".join(data[i+1:j])

        extra = '' if len(data) == j+1 else data[j+1]

        if team1 not in teamsdict:
            teamsdict[team1] = nteams
            nteams += 1

        if team2 not in teamsdict:
            teamsdict[team2] = nteams
            nteams += 1

        if 'N' in extra or 'n' in extra:
            neutgames[teamsdict[team1], teamsdict[team2]] += score1
            neutgames[teamsdict[team2], teamsdict[team1]] += score2

        else:
            awaygames[teamsdict[team1], teamsdict[team2]] += score1
            homegames[teamsdict[team2], teamsdict[team1]] += score2

    homegames = homegames[:nteams,:nteams]
    awaygames = awaygames[:nteams,:nteams]
    neutgames = neutgames[:nteams,:nteams]
    mats = (homegames, awaygames, neutgames)

    return teamsdict, mats
