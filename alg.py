# alg class
from numpy import array, empty, linalg, zeros, outer, tensordot
from numpy import abs as nabs
from datetime import datetime

class alg:
    def __init__(self, mat):
        self.mat = mat
        self.l = len(self.mat)
        self.conts = empty((self.l, self.l))

    def minimize(self):
        for i in xrange(self.l):
            self.conts[i][i] = sum(sum(p*p for p in
                self.mat[j][i]) for j in xrange(self.l))
            for j in xrange(i+1, self.l):
                tmp = -sum(p1*p2 for p1, p2 in zip(self.mat[i][j],
                    self.mat[j][i]))

                self.conts[i][j] = tmp
                self.conts[j][i] = tmp

        a = linalg.svd(self.conts)

        self.vec = nabs(a[-1][-1])

        m = max(self.vec)
        self.vec /= m
        return self.vec

    def contribution(self, i, j):
        return -self.conts[i][j]/self.conts[i][i]

    def E(self):
        return tensordot(outer(self.vec, self.vec), self.conts)
