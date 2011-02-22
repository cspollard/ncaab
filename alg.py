# alg class
from numpy import array, ones
from numpy.random import randn
from scipy.optimize import fmin_ncg as fmin
from team import team
from game import game
from datetime import datetime
from math import sqrt

debug = True

class alg:
    def __init__(self, scores):
        self.scores = scores

    def minimize(self):
        l = len(self.scores)
        return fmin(f, (ones(l) + randn(l)/10.)/sqrt(34.6), f1,
                fhess=f2, args=(self.scores,), maxiter=100,
                callback=cb)

def f(vec, mat):
    s = 0
    r = 0
    for i in xrange(len(vec)):
        for j in xrange(i+1, len(vec)):
            s += (mat[j][i]*vec[i] - mat[i][j]*vec[j])**2
        r += vec[i]**2
    return .5*(s + 1000*(r-10)**2)

def f1(vec, mat):
    return array([f1i(vec, mat, i) for i in
        xrange(len(vec))])

def f1i(vec, mat, i):
    return sum([(mat[j][i]*vec[i]-mat[i][j]*vec[j])*mat[j][i] for
        j in xrange(len(vec))]) + 1000*(vec[i]**3 - 10*vec[1])

def f2(vec, mat):
    return array([[f2ij(vec, mat, i, j) for j in
        xrange(len(vec))] for i in xrange(len(vec))])

def f2ij(vec, mat, i, j):
    return -mat[i][j]*mat[j][i] + 3000*vec[i]**2 - 10000

def cb(vec):
    print vec
