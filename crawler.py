# imports ncaabb data from kenpom.com
from subprocess import call
from numpy import zeros, resize
from scipy.sparse import csr_matrix

def crawl(filename=None, url=None, update=0, bb=1):
    if not filename:
        filename = "cbbga12.txt" if bb else "cfb2011stats.csv"
    if not url:
        url = "http://kenpom.com/cbbga12.txt"if bb else \
                "http://www.repole.com/sun4cast/stats/cfb2011stats.csv"
    if update:
        call(["rm", filename])
        call(["wget", url])

    f = open(filename)
    games = f.readlines()
    f.close()

    return crawl_bb(games) if bb else crawl_fb(games)

def crawl_bb(games):
    nteams = 0
    teamsdict = {}
    homegames = zeros((700,700))
    awaygames = zeros((700,700))
    neutgames = zeros((700,700))

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


def crawl_fb(games):
    nteams = 0
    teamsdict = {}
    homegames = zeros((500,500))
    awaygames = zeros((500,500))
    neutgames = zeros((500,500))

    for g in games[1:]:
        data = g.split(',')[1:]

        if data[1] == ' ':
            continue

        # get the teams and scores from the game.
        team1 = data[0]
        score1 = int(data[1])

        team2 = data[9]
        score2 = int(data[10])


        extra = '' if len(data) < 19 else data[18]

        if team1 not in teamsdict:
            teamsdict[team1] = nteams
            nteams += 1

        if team2 not in teamsdict:
            teamsdict[team2] = nteams
            nteams += 1

        if 'N' in extra or 'n' in extra:
            neutgames[teamsdict[team1], teamsdict[team2]] += score1
            neutgames[teamsdict[team2], teamsdict[team1]] += score2

        elif 'V' in extra:
            awaygames[teamsdict[team1], teamsdict[team2]] += score1
            homegames[teamsdict[team2], teamsdict[team1]] += score2

        elif 'H' in extra:
            homegames[teamsdict[team1], teamsdict[team2]] += score1
            awaygames[teamsdict[team2], teamsdict[team1]] += score2

    homegames = homegames[:nteams,:nteams]
    awaygames = awaygames[:nteams,:nteams]
    neutgames = neutgames[:nteams,:nteams]
    mats = (homegames, awaygames, neutgames)

    return teamsdict, mats
