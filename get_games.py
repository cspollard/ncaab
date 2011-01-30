# crawls http://www.rpiforecast.com/live-rpi.html for games.
from BeautifulSoup import BeautifulSoup, SoupStrainer
from urllib2 import urlopen
import re
from datetime import datetime
from game import game

# TODO
# this could be better.

def games_from_url(url):
    team = url.split('/')[-1][0:-5]
    u = urlopen(url)
    tmp = u.read()


    tmp1 = BeautifulSoup(tmp)
    tbl = tmp1.find(lambda tag: tag.tr and tag.tr.td and
            tag.tr.td.string and tag.tr.td.string == "Date")

    tmp = tbl.findChildren(lambda tag: tag.findAll("a",
        href=re.compile("/teams/")), recursive=False)

    games = []
    for g in tmp:
        curr = g.td
        (month, day) = [int(i) for i in curr.string.split("-")]
        now = datetime.now()
        year = now.year
        if month > 7:
            year -= 1
        date = datetime(year, month, day)
        if date > now:
            continue

        curr = g.find("a")
        opp = curr.string
        curr = g.findAll(text=re.compile("[0-9]*\-[0-9]*"))[-1]
        scores = [int(i) for i in curr.string.split("-")]
        if scores == [0, 0]:
            continue

        curr = g.find("td", text=re.compile("^[AHN]$"))
        if curr.string == "A":
            home = 1
        elif curr.string == "H":
            home = 0
        else:
            home = -1

        games.append(game(date, [team, opp], scores, home))

    return games


rooturl = "http://www.rpiforecast.com/live-rpi.html"
tmp = urlopen(rooturl)
tmp = tmp.read()
rootbs = BeautifulSoup(tmp)
tmp = rootbs.findAll("a", href=re.compile("/teams/"))
urllist = [tag['href'] for tag in tmp]

games = games_from_url(urllist[0])

for game in games:
    print game.home_team()
