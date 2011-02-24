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
            self.load_from_file(filename)
        else:
            self.rooturl = "http://kenpom.com/cbbga11.txt"
            self.teamsdict = {} 
            self.gamesdict = {} 
            self.initialize()

    def load_from_file(self, filename):
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

    def initialize(self):
        print "initializing..."
        stdout.flush()
        tmp = urllib2.urlopen(self.rooturl)
        lines = tmp.read().split('\n')

        for line in lines:
            data = line.split()
            scores = []
            i = 2
            while 1:
                try:
                    scores.append(int(data[i]))
                    break
                except ValueError:
                    i += 1

            if i == 2:
                teamname1 = data[1]
            else:
                teamname1 = " ".join(data[1:i])

            print teamname1
            if teamname1 not in self.teamsdict:
                self.teamsdict[teamname1] = team(teamname1)

            j = i+2
            while 1:
                try:
                    scores.append(int(data[j]))
                    break
                except ValueError:
                    j += 1

            if j == i+2:
                teamname2 = data[j]
            else:
                teamname2 = " ".join(data[i+2:j])

            print teamname2
            if teamname2 not in self.teamsdict:
                self.teamsdict[teamname2] = team(teamname2)

            teams = [self.teamsdict[teamname1], self.teamsdict[teamname2]]
            scores = [int(data[i+1]), int(data[j+1])]

            d = datetime.strptime(data[0], "%m/%d/%Y")

            if len(data) > 5:
                if data[5] == 'N':
                    home = -1
                else:
                    home = 1

            g = game(date, teams, scores, home)
            self.gamesdict[g.idx()] = g

            self.teamsdict[data[1]].add_games[[g]]
            self.teamsdict[data[3]].add_games[[g]]

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
        return self.teams

    def games(self):
        return self.games

