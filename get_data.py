import crawler
import threading
import time

a = crawler.crawler()

a.crawl(20)

while threading.active_count() > 1:
    time.sleep(1)

a.save("crawler.save")
