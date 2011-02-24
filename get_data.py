import crawler
from sys import argv

if len(argv) < 2:
    print "please provide a filename to save to."
    exit()

a = crawler.crawler()

a.save(argv[1])
