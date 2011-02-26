from sys import argv
from ROOT import *

f = open(argv[1])

lines = f.readlines()

f.close()

for i in xrange(len(lines)):
    if lines[i].startswith("Team"):
        columns = lines[i].replace(' ', '').split(',')
        data = lines[i+2:]

for i in xrange(len(data)):
    data[i] = data[i].replace(' ', '').split(',')

rankings_names = columns[8:]
rankings_names.pop(-1)
rankings_string = "int " + "; int ".join(rankings_names) + ";"
struct_string = "struct ncaatree {\
        char name[64];\
        char conf[4];\
        int nwins;\
        int nlosses;\
        int rank;\
        float mean;\
        float trimmed;\
        float median;\
        float stddev;\
        %s};" % rankings_string

gROOT.ProcessLine(struct_string)

from ROOT import ncaatree

n = ncaatree()
t = TTree("ncaatree", "tree of massey college basketball rankings")

t.Branch("name", AddressOf(n, "name"), "name/C")
t.Branch("conf", AddressOf(n, "conf"), "conf/C")
t.Branch("nwins", AddressOf(n, "nwins"), "nwins/I")
t.Branch("nlosses", AddressOf(n, "nlosses"), "nlosses/I")
t.Branch("rank", AddressOf(n, "rank"), "rank/I")
t.Branch("mean", AddressOf(n, "mean"), "mean/F")
t.Branch("trimmed", AddressOf(n, "trimmed"), "trimmed/F")
t.Branch("median", AddressOf(n, "median"), "median/F")
t.Branch("stddev", AddressOf(n, "stddev"), "stddev/F")

for ranking_name in rankings_names:
    t.Branch(ranking_name, AddressOf(n, ranking_name), ranking_name + "/I")

for line in data:
    n.name = line[0]
    n.conf = line[1]
    n.nwins, n.nlosses = map(int, line[2].split('-'))
    n.rank = int(line[3])
    n.mean = float(line[4])
    n.trimmed = float(line[5])
    n.median = float(line[6])
    n.stddev = float(line[7])
    for i in xrange(len(rankings_names)):
        try:
            exec "n.%s = int(line[%d])" % (rankings_names[i], 8+i)
        except ValueError:
            exec "n.%s = 0" % rankings_names[i]

    t.Fill()

f = TFile(argv[2], "RECREATE")
f.cd()
t.Write()
f.Close()
