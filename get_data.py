import crawler
from sys import argv

if len(argv) < 2:
    print "please provide a filename in which to save the information."
    exit()

if len(argv) > 2:
    url = argv[2]
    print "Getting data from", url
else:
    url = None

a = crawler.crawler(url=url)

a.save(argv[1])
