from network import node, edge, network

class ncaanetwork:
    def __init__(self, teams, games):
        self.network = network(len(teams))
        self.teams = teams
        self.games = games
        self.tdict = dict(zip(teams, self.network.nodes))
        for g in games:
            self.network.edge(self.tdict[g.winner()],
                    self.tdict[g.loser()]).setival(self.tdict[g.winner()],
                            g.winner_score())
            self.network.edge(self.tdict[g.loser()],
                    self.tdict[g.winner()]).setival(self.tdict[g.loser()],
                            g.loser_score())

        for i in xrange(10):
            for m in self.network.nodes:
                for n in self.network.nodes:
                    update(m, n, .1)

        self.network.dump()

        for t in self.tdict:
            print t.name() + ":", self.tdict[t].idx
