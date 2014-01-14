#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
A simple PyLucene Search Engine with allows you to index a webpage and do a search on the indexed elements.


Copyright © 2014 Soeren Kroell, Marco Wrzalik

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
documentation files (the "Software"), to deal in the Software without restriction, including without limitation 
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions 
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED 
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
DEALINGS IN THE SOFTWARE.
'''

import sys
import urllib2
import time
import socket
import nltk
from bs4 import BeautifulSoup
import lucene

# Global Variables
URL = 'http://www.spiegel.de'
SEARCHDEPTH = 1;
DIR = './index-data'


#PAGE
##################################

class Page(object):
    '''
    Creates a page with html, url, title, description, created and modified
    '''

    def __init__(self, html=None, url=None, title=None, description=None, created=None, modified=None, raw=None, tokens=None):
        '''
        Inits a page
        '''
        self.html = html
        self.url = url
        self.title = title
        self.description = description
        self.created = created
        self.modified = modified 



#SPIDER
##################################

class Spider(object):
    '''
    Creates a spider which opens a HTTP URL and analyses this document by getting out the content, title,
    description. These elemts will be stored in a Page() instance. After standardizing the url, the url 
    will also be stored in the page instance.

    All founded Pages are hold in a Pages dict, so that every page get´s only one time stored.
    '''
    
    def __init__(self, start_url):
        '''
        Inits a spider with an start URL.
        '''
        self.start_url = start_url
        self.pages = {}
    
    
    def initSpider(self, docurl):
        '''
        From the start URL, the spider go through all Hyperlinks it founds and analyses this pages also.
        All calls are recursive. 
        '''
        
        # open an URL
        try:
            response = urllib2.urlopen(docurl)
        except urllib2.HTTPError, error:
            print "HTTP error: %r" % error.code
            response = urllib2.urlopen(URL)
        except Exception, error:
            print "Error: %r" % error
            response = urllib2.urlopen(URL)

        # Get the DOM and close the response
        html = response.read()
        response.close() 
        
        # Go through the given DOM and get title and so on
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

        # For all founded Hyperlinks, standardize them, so they look all the same
        # If the spider founds a new url, it calls his self recursivly.
        for link in soup.find_all('a'):
            if len(self.pages) >= 40 :
                return
            url = str(link.get('href'))
            try:
                if url.startswith('/') or url.startswith(self.start_url):
                    if url.startswith('/'):
                        url = self.start_url + url[1:]
                    if not url.endswith('/'):
                        url = url.rstrip('/') # strip '/' at the end
                    if not self.pages.has_key(url):
                        print url
                        time.sleep(0.2) # take a sleep so the spider never gets blocked by the webpage
                        self.initSpider(url)
            except Exception, error:
                print "The Spider has done something boring: %r" % error
    
    
    def preparePage(self):
        '''
        Cleans the DOM to his raw form.
        '''
        for page in self.pages.values():
            page.raw = nltk.clean_html(page.html)
  
        

#WRITER
##################################

class Writer(object):
    '''
    Creates a Writer which can index given documents to definied folder.
    '''
    
    def __init__(self):
        '''
        Inits a Writer by attaching the current luceneVM to the thread and creating a analyzer, a store and a IndexWriter instance.
        '''
        vm_env = lucene.getVMEnv() # get lucene.vm
        vm_env.attachCurrentThread()
        self.analyzer = lucene.GermanAnalyzer(lucene.Version.LUCENE_CURRENT)
        self.store = lucene.SimpleFSDirectory(lucene.File(DIR))
        self.writer = lucene.IndexWriter(self.store, self.analyzer, True, lucene.IndexWriter.MaxFieldLength(512))
        
    def addPage(self, page):
        '''
        Adds a Page to a lucene document and indexing the url, description, content and title.
        '''
        doc = lucene.Document()
        doc.add(lucene.Field('url', page.url, lucene.Field.Store.YES, lucene.Field.Index.NOT_ANALYZED))
        if (page.description):
            doc.add(lucene.Field('description', page.description, lucene.Field.Store.YES, lucene.Field.Index.ANALYZED))
        doc.add(lucene.Field('content', page.raw, lucene.Field.Store.YES, lucene.Field.Index.ANALYZED))
        doc.add(lucene.Field('title', page.title, lucene.Field.Store.YES, lucene.Field.Index.ANALYZED))
        self.writer.addDocument(doc)

    def getDoc(self, index):
        '''
        Returns a requested Document
        '''
        return self.store.values()[index]

    def close(self):
        '''
        Closes the current writer and set´s it null.
        '''
        print "Currently are "+ str(self.writer.numDocs()) +" documents indexed. Indexing done!" 
        self.writer.optimize()
        self.writer.close()
        self.writer = None


    


#READER
##################################
class Reader(object):
    '''
    Creates a Read, which provides the possibilty to read an indexed file.
    '''

    def __init__(self):
        '''
        Inits a Reader by attaching the current luceneVM to the thread and creating a store and a IndexReader instance.
        '''
        vm_env = lucene.getVMEnv() # get lucene.vm
        vm_env.attachCurrentThread()
        self.store = lucene.SimpleFSDirectory(lucene.File(DIR))
        self.reader = lucene.IndexReader.open(self.store, True)

    def getIndexedPages(self):
        '''
        Returns a HTML formatted DIV with the number of already indexed files and UL with LI elements, which contains 
        the item url.
        '''
        terms = self.reader.terms(lucene.Term("url", ""))
        facets = {'other': 0}
        temp = "<div><p class='lead'>Derzeit sind "+ str(self.reader.numDocs()) +" Dokumente indexiert.</p></div>" 
        temp += "<ul>"
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
    '''
    Creates a Searcher to find a query inside an indexed file.
    '''

    def __init__(self):
        '''
        Inits a Searcher by attaching the current luceneVM to the thread and creating a analyzer, a store, a parser and a IndexSearcher instance.
        '''
        vm_env = lucene.getVMEnv()
        vm_env.attachCurrentThread()
        self.analyzer = lucene.GermanAnalyzer(lucene.Version.LUCENE_CURRENT)
        self.store = lucene.SimpleFSDirectory(lucene.File(DIR))
        self.parser = lucene.MultiFieldQueryParser(
            lucene.Version.LUCENE_CURRENT,
            ["content"],
            self.analyzer)
        self.searcher = lucene.IndexSearcher(self.store, readOnly=True)


    def search(self, queryString):
        '''
        Do the actually search for the given queryString and returns an HTML formatted UL with the URL, Title, description and score doc.
        '''
        query = self.parser.parse(self.parser, queryString)
        scoredocs = self.searcher.search(query, 50).scoreDocs
        MAX = 1000
        hits = self.searcher.search(query, MAX)
        temp = '<p class="lead">Insgesamt wurde(n) ' + str(hits.totalHits) + ' Dokument(e) für die Suchanfrage "' + str(query) + '" gefunden.</p>'

        for hit in scoredocs:
            #print hit.score, hit.doc, hit.toString()
            doc = self.searcher.doc(hit.doc)
            temp += '<div style="margin-bottom:30px;"><ul class="list-unstyled"><li><h5><a href="' + doc.get("url").encode("utf-8") + '" target="_blank">'+ doc.get("title").encode("utf-8") +'</a></h5> </li><li><a href="'+ doc.get("url").encode("utf-8") +'">'+doc.get("url").encode("utf-8")+' </a></li><li>' + doc.get("description").encode("utf-8") +'</li><li> Score: <b>'+ str(hit.score)+'</b></li></ul></div>'
        return temp



#SEARCH ENGINE
##################################

class SearchEngine(object):
    '''
    Creates a Search Enginge and provides all necessary functions to start the spider, writer or do a search. 
    These functions are getting used in the WebServer.py 
    '''

    def __init__(self, URL=None):
        '''
        Inits a SearchEngine and creating the only lucene VM.
        '''
        lucene.initVM() # only initVM once!
        self.url = URL
        self.spider = None
        self.writer = None
        self.searcher = None

    def startSpider(self, URL=None):
        '''
        Starts the spider on the given URL
        '''
        spider = Spider(URL)
        spider.initSpider(URL)
        spider.preparePage()
        self.spider = spider

    def startWriter (self):
        '''
        Starts the Writer and add´s all founded pages to the spider.pages dict.
        '''
        writer = Writer()    
        [writer.addPage(p) for p in self.spider.pages.values()]
        writer.close()
        self.writer = writer

    def startSpiderAndIndex(self, threadName=None, URL=None):
        '''
        Is getting called in the WebServer.py to start the spider and indexing.
        '''
        print "########## The Spider is on her way! ##########"
        self.startSpider(self.url)
        print "########## Now just indexing da things ##########"
        self.startWriter()

    def startSearch (self, query):
        '''
        Is getting called in the WebServer.py to start a search
        '''
        searcher = Searcher()
        self.searcher = searcher
        return searcher.search(query)

    def getIndexedPages(self):
        '''
        Is getting called in the WebServer.py to get all indexed Pages
        '''
        reader = Reader()
        return reader.getIndexedPages()



    
