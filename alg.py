# alg class
from numpy import array, empty, linalg, zeros
from numpy import abs as nabs
from numpy.random import randn
from team import team
from game import game
from datetime import datetime
from math import sqrt

class alg:
    def __init__(self, mat):
        self.mat = mat
        self.l = len(self.mat)
        self.vec = empty(self.l)
        self.conts = empty((self.l, self.l))

    def minimize(self):
        for i in xrange(self.l):
            for j in xrange(self.l):
                if i == j:
                    self.conts[i][j] = sum([sum(p**2 for p in
                        self.mat[i][k]) for k in xrange(self.l)])
                else:
                    self.conts[i][j] = -sum(p1*p2 for (p1,p2) in
                            zip(self.mat[i][j], self.mat[j][i]))

        a = linalg.svd(self.conts)

        self.vec = nabs(a[-1][-1])

        m = max(self.vec)
        self.vec /= m
        return self.vec

    def contribution(self, i, j):
        return self.conts[i][j]/self.conts[i][i]

    def E(self):
        return 0
