#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 06.12.2013
@author: soerenkroell
'''

# from model import Page
import sys
import json
import cgi
import urllib2
import time
import socket
import nltk
from bs4 import BeautifulSoup
import lucene                    
 


URL = 'http://www.spiegel.de/'
SEARCHDEPTH = 1;


# PAGE MODEL
##################################

class Page(object):
    '''
    classdocs
    '''

    def __init__(self, html=None, url=None, title=None, description=None, created=None, modified=None, raw=None, tokens=None):
        '''
        Constructor
        '''
        self.html = html
        self.url = url
        self.title = title
        self.description = description
        self.created = created
        self.modified = modified 







#SPIDER MODEL
##################################

class Spider(object):
    
    def __init__(self, start_url):
        '''
        Constructor
        '''
        self.start_url = start_url
        self.pages = {} # günstigere Suche wegen Hashing
    
    
    def initSpider(self, docurl):
    
        try:
            #response = urllib2.urlopen(docurl,timeout=5)
            response = urllib2.urlopen(docurl)
        except urllib2.HTTPError, error:
            print "HTTP error: %r" % error.code
            response = urllib2.urlopen(URL)
        except Exception, error:
            print "Error: %r" % error
            response = urllib2.urlopen(URL)

    
        html = response.read()
        response.close() 
        
        soup = BeautifulSoup(html)
        title = soup.title.string
        description = soup.find("meta", {"property":"og:description"})
        if(description):
            description = description['content']
        else:
            description = soup.find("meta", {"name":"description"})
            if (description):
                description = description['content']
        created = modified = time.time()
        page = Page(html, docurl, title, description, created, modified)
        self.pages[docurl]= page

        for link in soup.find_all('a'):
            if len(self.pages) >= 7 :
                return
            url = str(link.get('href'))
            try:
                if url.startswith('/') or url.startswith(self.start_url):
                    if url.startswith('/'):
                        url = self.start_url + url[1:]
                        #print "URL-", url
                    url = url.rstrip('/') # '/' am ende entfernen
                    if not self.pages.has_key(url):
                        print url
                        time.sleep(0.2) 
                        self.initSpider(url)
            except Exception, error:
                print "Error: %r" % error
        
    
    def preparePage(self):
        print len(self.pages)
        for page in self.pages.values():
            page.raw = nltk.clean_html(page.html)
            '''Wird Lucene schon machen'''
            #page.tokens = nltk.word_tokenize(page.raw)
  
        
    

class Indexer(object):
    
    def __init__(self):
        lucene.initVM()
        self.analyzer = lucene.StandardAnalyzer(lucene.Version.LUCENE_CURRENT)
        self.store = lucene.SimpleFSDirectory(lucene.File('./data/'))
        self.writer = lucene.IndexWriter(self.store,
                                             self.analyzer,
                                             True,
                                             lucene.IndexWriter.MaxFieldLength(512))
        

    def addPage(self, page):
        doc = lucene.Document()
        doc.add(lucene.Field('url', page.url,
                             lucene.Field.Store.YES,
                             lucene.Field.Index.NOT_ANALYZED))
        if (page.description):
            doc.add(lucene.Field('description', page.description,
                                 lucene.Field.Store.YES,
                                 lucene.Field.Index.ANALYZED))
        doc.add(lucene.Field('content', page.raw,
                             lucene.Field.Store.YES,
                             lucene.Field.Index.ANALYZED))
        self.writer.addDocument(doc)

    def getDoc(self, index):
        return self.store.values()[index]

    def close(self):
        self.writer.optimize()
        self.writer.close()
        self.writer = None



print "Content-Type: text/html;charset=utf-8\n"


# spider = Spider(URL)
print "start crawling...\n"

# spider.initSpider(URL)
# print "\n...finished crawling\n"
# spider.preparePage()

# indexer = Indexer()
# print "indexing pages"
    
# [indexer.addPage(p) for p in spider.pages.values()] indexer.close()

# searcher = Searcher(indexer)
# eingabe = "";



# request = cgi.FieldStorage()
# searchRequest = request["searchquery"].value

# print searcher.search(searchRequest)

   


    
