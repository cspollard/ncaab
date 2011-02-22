# alg class
from numpy import array, ones
from numpy.random import randn
from scipy.optimize import fmin_ncg as fmin
from team import team
from game import game
from datetime import datetime
from math import sqrt

debug = False

class alg:
    def __init__(self, mat):
        self.mat = mat
        self.l = len(self.mat)
        self.vec = (ones(self.l) + randn(self.l)/10)/sqrt(len(self.mat))

    def minimize(self):
        k = 0
        while k < 50:
            k += 1
            for i in xrange(self.l):
                a = sum([self.mat[j][i] for j in xrange(self.l)])
                b = sum([self.mat[i][j]*self.vec[j] for j in
                    xrange(self.l)])
                self.vec[i] = b/a

                # print self.vec[i]

        return self.vec
