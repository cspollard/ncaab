from random import randint

DEBUG = True


class node:
    def __init__(self, idx):
        self.idx = idx
        self.edges = {}

    def __gt__(self, n):
        return self.idx > n.idx

    def __eq__(self, n):
        return self.idx == n.idx

    def __lt__(self, n):
        return self.idx < n.idx

    def edge(self, n):
        return self.edges[n]


class edge:
    def __init__(self, m, n):
        self.nodes = [m, n]
        n.edges[m] = self
        m.edges[n] = self

        self.values = {m: 0.0, n: 0.0}
        self.ivals = {m: 0.0, n: 0.0}

    def set(self, n, v, w):
        self.values[n] = (self.ivals[n] + w*v)/(1 + w)

    def value(self, n):
        return self.values[n]

    def othernode(self, n):
        if n is self.nodes[0]:
            return self.nodes[1]
        else:
            return self.nodes[0]

    def inedge(self, n):
        return n in self.nodes


class network:
    def __init__(self, l):
        self.nodes = []

        # instantiate all nodes.
        self.nodes = map(lambda i: node(i), xrange(l))

        # instantiate all edges.
        for m in self.nodes:
            for n in self.nodes:
                if m < n:
                    edge(m, n)

    def edge(self, m, n):
        return m.edge(n)

    def update(self, k, l, y):
        tmp = 0.0
        w = 0
        for m in k.edges.keys():
            if m is l:
                continue

            a = k.edge(m).value(k)
            if a < 1:
                continue

            for n in m.edges.keys():
                if (n is k) or (n is l):
                    continue

                b = m.edge(n).value(n)
                c = n.edge(l).value(n)
                if b < 1 or c < 1:
                    continue

                tmp += a*c/b
                w += y

        edge(k, l).set(k, tmp, w)

    def dump(self):
        for m in nodes:
            print "node %3d:" % m.idx
            for n in nodes:
                if m is not n:
                    e = self.edge(m, n)
                    print "\t%03.0f\t%03.0f: node %03d" % (e.value(m),
                            e.value(n), n.idx)
