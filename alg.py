# alg class
from numpy import array, empty, linalg, zeros
from numpy import abs as nabs
from numpy.random import randn
from team import team
from game import game
from datetime import datetime
from math import sqrt

debug = False

class alg:
    def __init__(self, mat):
        self.mat = array(mat)
        self.l = len(self.mat)
        self.vec = empty(self.l)
        self.conts = empty((self.l, self.l))
        self.colsums = self.mat.sum(axis=0)

    def minimize(self):
        for i in xrange(self.l):
            for j in xrange(self.l):
                if i == j:
                    self.conts[i][j] = -self.colsums[i]
                else:
                    self.conts[i][j] = self.mat[i][j]

        a = linalg.svd(self.conts)

        self.vec = nabs(a[-1][-1])

        m = max(self.vec)
        self.vec /= m
        return self.vec

    def contribution(self, i, j):
        return self.mat[i][j]*self.vec[j]/self.colsums[i]

    def E(self):
        return .5*sum([sum([self.mat[j][i]*self.vec[i] -
            self.mat[i][j]*self.vec[j] for j in xrange(i+1, self.l)])
            for i in xrange(self.l)])**2
