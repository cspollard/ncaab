# alg class
from numpy import array, ones
from numpy.random import randn
from scipy.optimize import fmin_ncg as fmin
from team import team
from game import game
from datetime import datetime
from math import sqrt
from random import choice

debug = False

class alg:
    def __init__(self, mat):
        self.mat = array(mat)
        self.l = len(self.mat)
        self.vec = randn(self.l)**2
        self.colsums = self.mat.sum(axis=0)

    def minimize(self, kmax=50000):
        k = 0
        ls = list(xrange(self.l))
        while k < kmax:
            k += 1
            i = choice(ls)
            self.vec[i] = sum([self.mat[i][j]*self.vec[j] for j in
                    xrange(self.l)])/self.colsums[i]

        m = max(self.vec)
        self.vec /= m
        return self.vec

    def contribution(self, i, j):
        return self.mat[i][j]*self.vec[j]/self.colsums[i]

    def E(self):
        return .5*sum([sum([self.mat[j][i]*self.vec[i] -
            self.mat[i][j]*self.vec[j] for j in xrange(i+1, self.l)])
            for i in xrange(self.l)])**2
