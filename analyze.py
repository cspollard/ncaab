# analyzes data coming from the crawler.
from crawler import crawl

(teamsdict, (homescores, awayscores, neutscores)) = crawl(update=1)
