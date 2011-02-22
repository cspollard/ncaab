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
        self.mat = mat
        self.l = len(self.mat)
        self.vec = (ones(self.l) + randn(self.l)/10)/sqrt(len(self.mat))

    def minimize(self):
        k = 0
        ls = list(xrange(self.l))
        while k < 50000:
            k += 1
            i = choice(ls)
            a = sum([self.mat[j][i] for j in xrange(self.l)])
            b = sum([self.mat[i][j]*self.vec[j] for j in
                xrange(self.l)])
            self.vec[i] = b/a

        return self.vec
