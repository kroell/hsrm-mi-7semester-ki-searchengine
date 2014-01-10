'''
Created on 06.12.2013

@author: soerenkroell
'''

from model import Spider, Indexer, Searcher
import sys

URL = 'http://www.spiegel.de/'



if __name__ == '__main__':

    spider = Spider(URL)
    print "start crawling...\n"
    spider.initSpider(URL)
    print "\n...finished crawling\n"
    spider.preparePage()
    #print len(spider.pages) #330
    indexer = Indexer()
    print "indexing pages"
    
    [indexer.addPage(p) for p in spider.pages.values()]
    indexer.close()

    searcher = Searcher(indexer)
    eingabe = "";
    while (True):
        print "Geben sie Ihren Suchgebriff ein"
        eingabe = sys.stdin.readline()
        if eingabe == "exit": break;
        searcher.search(eingabe);
    
    
   
