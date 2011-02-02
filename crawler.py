# crawler class

import re
import urllib2
from threading import Thread, Lock
import BeautifulSoup
import pickle
from sys import stdout
from datetime import datetime
from team import team
from game import game

class crawler:
    def __init__(self, filename=None):
        if filename:
            self._load_from_file(filename)
        else:
            self._rooturl = "http://www.rpiforecast.com/live-rpi.html"
            self._urllist = []
            self._teams = {} 
            self._games = {} 
            self._initialize()

    def _load_from_file(self, filename):
        f = open(filename, "r")
        lines = f.readlines()
        f.close()

        self._teams = {}
        self._games = {}

        for line in lines:
            tmp = line.split(',')
            year = int(tmp[0][:4])
            month = int(tmp[0][4:6])
            day = int(tmp[0][6:])
            date = datetime(year, month, day)
            t1 = self._teams.setdefault(tmp[1], team(tmp[1]))
            t2 = self._teams.setdefault(tmp[2], team(tmp[2]))
            scores = map(int, tmp[3:5])
            home = int(tmp[5])
            g = game(date, [t1, t2], scores, home)
            self._games.setdefault(g.idx(), g)
            t1.add_games([g])
            t2.add_games([g])


    def _initialize(self):
        print "initializing..."
        tmp = urllib2.urlopen(self._rooturl)
        tmp = BeautifulSoup.BeautifulSoup(tmp.read()).findAll("a",
                href=re.compile("/teams/"))

        self._urllist = [tag["href"] for tag in tmp]
        for url in self._urllist:
            teamname = url.split('/')[-1][0:-5]
            t = team(teamname)
            self._teams.setdefault(teamname, t)

    def crawl(self, nthreads):

        locks = []
        threads = []
        i = 0
        while i < nthreads:
            locks.append(Lock())
            i += 1

        i = 0
        for t in self._teams.itervalues():
            threads.append(Thread(target=self.get_games, args=(t,
                locks[i % nthreads])))
            threads[i].start()
            i += 1

    def get_games(self, t, lock=None):
        if lock:
            lock.acquire()

        # TODO
        # this is ugly.
        url = "http://www.rpiforecast.com/teams/%s.html" % t.name()
        url = urllib2.quote(url, safe="%/:=&?~#+!$,;'@()*[]")
        try:
            tmp = urllib2.urlopen(url)
        except urllib2.HTTPError:
            print "couldn't reach %s.\nexiting thread." % url
            lock.release()
            return

        print "retrieving data for %s..." % t.name()

        tmp = BeautifulSoup.BeautifulSoup(tmp.read())
        tmp = tmp.find(lambda tag: tag.tr and tag.tr.td and
            tag.tr.td.string and tag.tr.td.string == "Date")
        tmp = tmp.findChildren(lambda tag: tag.findAll("a",
            href=re.compile("/teams/")), recursive=False)

        tmpgames = []
        for g in tmp:
            numbers = g.findAll(text=re.compile("[0-9]+\-[0-9]+"))
            scores = map(int, numbers[-1].string.split("-"))
            if scores == [0, 0]:
                continue

            # account for larger score always coming first.
            if g.find("td", text=re.compile("^[L]$")):
                scores.reverse()

            opp = g.find("a")["href"].split('/')[-1][0:-5]
            if opp not in self._teams:
                continue

            opp = self._teams[opp]
            if opp.is_locked():
                continue

            (month, day) = map(int, numbers[0].string.split('-'))
            year = datetime.now().year
            if month > 7:
                year -= 1
            date = datetime(year, month, day)

            home = {"A":1, "H":0, "N":-1}[g.find("td",
                text=re.compile("^[AHN]$")).string]

            tmpgame = game(date, [t, opp], scores, home)
            if tmpgame.idx() not in self._games: 
                self._games[tmpgame.idx()] = tmpgame
                tmpgames.append(tmpgame)
                opp.add_games([tmpgame])

                print tmpgame.teams()[0].name(), "vs", \
                    tmpgame.teams()[1].name(), '\t', \
                    tmpgame.scores()[0], '-', tmpgame.scores()[1]

                stdout.flush()
            else:
                print t.name(), "vs", opp.name(), \
                    tmpgame.date().strftime("%Y %m %d"), "already in \
                    database. ignoring..."

        t.add_games(tmpgames)
        print "finished retrieving data for %s." % t.name()
        print len(self._games), "indexed so far."

        t.lock()

        if lock:
            lock.release()

    def save(self, filename):
        f = open(filename, "w")
        for game in self._games.itervalues():
            f.write("%s,%s,%s,%3d,%3d,%2d\n" %
                    (game.date().strftime("%Y%m%d"),
                        game.teams()[0].name(),
                        game.teams()[1].name(), game.scores()[0],
                        game.scores()[1], game.home()))

        f.close()

    def teams(self):
        return self._teams

    def games(self):
        return self._games

