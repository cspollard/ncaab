# team class.
from game import game
from hashlib import new as newhash

class team:
    def __init__(self, name):
        self._name = name
        self._idx = newhash(name).hexdigest()
        self._games = []
        self._ngames = 0
        self._nwins = 0
        self._nlosses = 0
        self._opponents = []
        self._wfrac = 0
        self._lfrac = 0
        self._is_locked = False

    def __eq__(self, t):
        return self.idx() == t.idx()

    def _update(self):
        self._ngames = 0
        self._nwins = 0
        self._nlosses = 0
        self._opponents = []
        self._wfrac = 0
        self._lfrac = 0

        for game in self._games:
            if not self._in_game(game):
                self._games.remove(game)
                continue
            elif self._did_win(game):
                self._nwins += 1
            else:
                self._nlosses += 1

        self._ngames = len(self._games)
        if self._ngames == 0:
            return

        self._opponents = map(self._opponent, games)
        self._wfrac = float(self._nwins) / float(self._ngames)
        self._lfrac = float(self._nlosses) / float(self._ngames)

    def _in_game(self, game):
        return self in game.teams()

    def _did_win(self, game):
        return game.winner() == self

    def _opponent(self, game):
        if game.teams[0] == self:
            return game.teams[1]
        else:
            return game.teams[0]

    def idx(self):
        return self._idx

    def is_locked(self):
        return self._is_locked

    def add_games(self, games):
        self._is_locked = True
        for game in games:
            if game not in self._games:
                self._games.append(game)

        self._update()
        self._is_locked = False
