#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Search Engine
'''

import sys
import urllib2
import time
import socket
import nltk
from bs4 import BeautifulSoup
import lucene

import thread



URL = 'http://www.spiegel.de/'
SEARCHDEPTH = 1;
DIR = './index-data'

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
            #if len(self.pages) >= 20 :
             #   return
            url = str(link.get('href'))
            try:
                if url.startswith('/') or url.startswith(self.start_url):
                    if url.startswith('/'):
                        url = self.start_url + url[1:]
                    if not url.endswith('/'):
                        url = url.rstrip('/') # '/' am ende entfernen
                    if not self.pages.has_key(url):
                        print url
                        time.sleep(0.2) 
                        self.initSpider(url)
            except Exception, error:
                print "The Spider has done something boring: %r" % error
    
    
    def preparePage(self):
        #print len(self.pages)
        for page in self.pages.values():
            page.raw = nltk.clean_html(page.html)
            '''Wird Lucene schon machen'''
            #page.tokens = nltk.word_tokenize(page.raw)
  

    def getIndexedPages(self):
        temp = "<ul>"
        for value in self.pages:
            print value
            temp += '<li><a href="'+ value +'" title="' + value + '">' + value + '</a></li>'

        temp += '</ul>'
        return temp
        

#WRITER
##################################

class Writer(object):
    
    def __init__(self):
        lucene.initVM()
        self.analyzer = lucene.StandardAnalyzer(lucene.Version.LUCENE_CURRENT)
        self.store = lucene.SimpleFSDirectory(lucene.File(DIR))
        self.writer = lucene.IndexWriter(self.store, self.analyzer, True, lucene.IndexWriter.MaxFieldLength(512))
        print "Currently there are %d documents in the index..." % self.writer.numDocs()
        
    def addPage(self, page):
        doc = lucene.Document()
        doc.add(lucene.Field('url', page.url, lucene.Field.Store.YES, lucene.Field.Index.NOT_ANALYZED))
        if (page.description):
            doc.add(lucene.Field('description', page.description, lucene.Field.Store.YES, lucene.Field.Index.ANALYZED))
        doc.add(lucene.Field('content', page.raw, lucene.Field.Store.YES, lucene.Field.Index.ANALYZED))
        doc.add(lucene.Field('title', page.title, lucene.Field.Store.YES, lucene.Field.Index.ANALYZED))
        self.writer.addDocument(doc)

    def getDoc(self, index):
        return self.store.values()[index]

    def close(self):
        self.writer.optimize()
        self.writer.close()
        self.writer = None

    


#READER
##################################
class Reader(object):

    def __init__(self):
        lucene.initVM()
        self.analyzer = lucene.StandardAnalyzer(lucene.Version.LUCENE_CURRENT)
        self.store = lucene.SimpleFSDirectory(lucene.File(DIR))
        self.reader = lucene.IndexReader.open(self.store, True)

    def getIndexedPages(self):
        terms = self.reader.terms(lucene.Term("url", ""))
        facets = {'other': 0}
        temp = "<ul>"
        while terms.next():
            if terms.term().field() != "url": 
                break
            #print "Field Name:", terms.term().field()
            #print "Field Value:", terms.term().text()
            #print "Matching Docs:", int(self.reader.docFreq(terms.term()))
            temp += '<li><a href="'+ terms.term().text().encode("utf-8") +'" title="' + terms.term().text().encode("utf-8") + '">' + terms.term().text().encode("utf-8") + '</a></li>'

        temp += '</ul>'
        return temp



#SEARCHER
##################################
class Searcher(object):

    def __init__(self):
        lucene.initVM()
        self.analyzer = lucene.StandardAnalyzer(lucene.Version.LUCENE_CURRENT)
        self.store = lucene.SimpleFSDirectory(lucene.File(DIR))
        self.parser = lucene.MultiFieldQueryParser(
            lucene.Version.LUCENE_CURRENT,
            ["content"],
            self.analyzer)
        self.searcher = lucene.IndexSearcher(self.store, readOnly=True)


    def search(self, queryString):
        query = self.parser.parse(self.parser, queryString)
        scoredocs = self.searcher.search(query, 50).scoreDocs
        MAX = 1000
        hits = self.searcher.search(query, MAX)
        #print 
        temp = '<p class="lead">Insgesamt wurden ' + str(hits.totalHits) + ' Dokument(e) für die Suchanfrage "' + str(query) + '" gefunden.</p>'

        for hit in scoredocs:
            print hit.score, hit.doc, hit.toString()
            doc = self.searcher.doc(hit.doc)
            temp += '<div style="margin-bottom:30px;"><ul class="list-unstyled"><li><h5><a href="' + doc.get("url").encode("utf-8") + '" target="_blank">'+ doc.get("title").encode("utf-8") +'</a></h5> </li><li><a href="'+ doc.get("url").encode("utf-8") +'">'+doc.get("url").encode("utf-8")+' </a></li><li>' + doc.get("description").encode("utf-8") +'</li><li> Score: '+ str(hit.score)+'</li></ul></div>'
 
        return temp





#SEARCH ENGINE MODEL
##################################

class SearchEngine(object):

    def __init__(self, URL=None):
        self.url = URL
        self.spider = None
        self.writer = None
        self.searcher = None

    def startSpider(self, URL=None):
        spider = Spider(URL)
        spider.initSpider(URL)
        spider.preparePage()
        self.spider = spider

    def startWriter (self):
        writer = Writer()    
        [writer.addPage(p) for p in self.spider.pages.values()]
        writer.close()
        self.writer = writer

    def startSpiderAndIndex(self, threadName=None, URL=None):
        print "The Spider is on her way!"
        self.startSpider(self.url)
        print "Now just indexing da things"
        self.startWriter()
        print "And we are done!"
        

    def startSearch (self, query):
        searcher = Searcher()
        self.searcher = searcher
        return searcher.search(query)

    def getSpider(self):
        return self.spider

    def getWriter(self):
        return self.writer

    def getSearcher(self):
        return self.searcher

    def getIndexedPages(self):
        reader = Reader()
        return reader.getIndexedPages()



    
