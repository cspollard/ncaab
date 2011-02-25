import crawler
from sys import argv

if len(argv) < 2:
    print "please provide a filename to save to."
    exit()

if len(argv) > 2:
    url = argv[2]
else:
    url = None

a = crawler.crawler(url=url)

a.save(argv[1])
