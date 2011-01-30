import crawler

a = crawler.crawler()
a.initialize()

a.crawl(5)

for game in a._games.itervalues():
    print game._date.strftime("%m-%d"), game._teams[0]._name, \
        game._teams[1]._name, "%d-%d" %(game._scores[0], \
                game._scores[1])

a.save_pickle("crawler.pickle")
