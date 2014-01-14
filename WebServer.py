#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
A simple CherryPy WebServer which provides you a search form from where you can send your search queries
to the search engine.
It show´s you which pages are already indexed an provides a hitlist of your query results with title,
url, description and hit-score.


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

import os

import thread
import cherrypy
import SearchEngine as engine

# Global Variables
URL = 'http://www.spiegel.de/'
searchEngine = engine.SearchEngine(URL) # create a searchEngine Instance
indexer = None


class StartPage(object):
    '''
    The StartPage provides in the index() a search form to send a search query. This form
    calls the search() function, which sends the start query to the SearchEngine. 

    Both run in a seperate Thread.
    '''

    def index(self):
        '''
        Calls the indexThread(), which starts indexing in the background. Also it provides a main html template
        with a search form.
        '''
        wd = cherrypy.process.plugins.BackgroundTask(30,self.indexThread) # start indexing in a seperate Thread
        wd.start()
        print "Indexing-Thread-Monster has been started..."
        return self.template()
        wd.cancel()
    index.exposed = True # necessary so this page/function can be visited

    def search(self, query=None):
        '''
        Gets called from the search form and starts a search of the given query. The result will be given
        inside a html template
        '''
        wd = cherrypy.process.plugins.BackgroundTask(1000,self.foo) # start indexing in a seperate Thread
        wd.start()
        print "Searching-Thread-Monster has been started..."
        queryResult = searchEngine.startSearch(query)
        return ('''<!doctype html>
<html lang="en" ng-app="app">
<head>
  <meta charset="UTF-8">
  <title>SearchSpiegel</title>
  <script src="https://code.jquery.com/jquery.js"></script>
  <link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css">
  <script src="//netdna.bootstrapcdn.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>
</head>
<body>
<div class="container">
      <div class="page-header text-center">
            <h1>Durchsuche Spiegel.de</h1>
            <p class="lead">Alles was du schon immer auf Spiegel.de finden wolltest, findest du <a href="/start/">hier</a>.</p>
      </div>
      <div>
      <form class="form-inline" role="form" method="post" action="search">
              <div class="col-md-10">
                <input type="text" class="form-control input-lg" id="queryInput" name="query" placeholder="Deine Suchanfrage" required>
              </div>
              
              <button type="submit" class="btn btn-primary btn-lg">Abschicken</button>
      </form>

      </div>
      <div id="answer" class="col-md-12"><br/>
%s
      </div>
</div>

<div id="footer" class="container text-center">
    <nav class="navbar navbar-default navbar-fixed-bottom">
        <div class="navbar-inner navbar-content-center">
          <p></p>
            <a href="/start/">Suchmaske</a> | <a href="/indexed_pages">Übersicht indexierte Seiten</a>
        </div>
    </nav>
</div>
<script>
    $(document).ready(function($){
      $('#submit').click(function (){
          $('#loader').show();
        });
    });
  </script>

</body></html>''') % queryResult
        wd.cancel()
    search.exposed = True # necessary so this page/function can be visited

    def template(self):
        '''
        Provides a HTML template with a search form. 
        '''
        template = '''<!doctype html>
<html lang="en" ng-app="app">
<head>
  <meta charset="UTF-8">
  <title>SearchSpiegel</title>
  <script src="https://code.jquery.com/jquery.js"></script>
  <link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css">
  <script src="//netdna.bootstrapcdn.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>
</head>

<body>
<div class="container">
      <div class="page-header text-center">
            <h1>Durchsuche Spiegel.de</h1>
            <p class="lead">Alles was du schon immer auf Spiegel.de finden wolltest, findest du <a href="/start/">hier</a>.</p>
      </div>
      <div class="searchBar">

      <form class="form-inline" role="form" method="post" action="search">

              <div class="col-md-10">
                <input type="text" class="form-control input-lg" id="queryInput" name="query" placeholder="Deine Suchanfrage" required>
              </div>
              
              <button type="submit" id="submit" class="btn btn-primary btn-lg">Abschicken</button>
      </form>
      </div>
      
      </br>
      </br>

      <div class="text-center">
        <img src="http://www.idseven.info/ajax-loader.gif" id="loader" style="display: none;"></img>
      </div>
  </div>
  <div id="footer" class="container text-center">
    <nav class="navbar navbar-default navbar-fixed-bottom">
        <div class="navbar-inner navbar-content-center">
          <p></p>
            <a href="/start/">Suchmaske</a> | <a href="/indexed_pages">Übersicht indexierte Seiten</a>
        </div>
    </nav>
</div>
 

    <script>
    $(document).ready(function($){
      $('#submit').click(function (){
          $('#loader').show();
        });
    });
  </script>
</body>
</html>'''
    	return template

    def indexThread(self):
        '''
        Inits the search engine spider and inits indexing of all found pages
        '''
        searchEngine.startSpiderAndIndex()

    def foo(self):
        '''
        Does nothing, put is necessary :-)
        '''
        return # foo is doing just nothing
        


class ShowIndexedPages(object):
    '''
    The ShowIndexedPages provides a list of all indexed URL.
    '''

    def index(self):
        '''
        Gets all indexed pages from the search engine
        '''
        wd = cherrypy.process.plugins.BackgroundTask(1000,self.foo)
        wd.start()
        indexedPages = searchEngine.getIndexedPages()
        return self.template(indexedPages)
        wd.cancel()
    index.exposed = True # necessary so this page/function can be visited

    def template(self, indexedPages):
        '''
        Provides a HTML template
        '''
        return '''<!doctype html>
<html lang="en" ng-app="app">
<head>
  <meta charset="UTF-8">
  <title>SearchSpiegel</title>
  <script src="https://code.jquery.com/jquery.js"></script>
  <link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css">
  <script src="//netdna.bootstrapcdn.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>
</head>
<body>
  <div class="container">
      <div class="page-header text-center">
            <h1>Alle indizierten Seiten</h1>
            <p class="lead">Alles was du schon immer auf Spiegel.de finden wolltest, findest du <a href="/start/">hier</a>.</p>
      </div>
      <div>
        %s
      </div>
      <div>

         
  </div>
  <div id="footer" class="container text-center">
    <nav class="navbar navbar-default navbar-fixed-bottom">
        <div class="navbar-inner navbar-content-center">
          <p></p>
            <a href="/start/">Suchmaske</a> | <a href="/indexed_pages">Übersicht indexierte Seiten</a>
        </div>
    </nav>
</div>
</body></html>''' % indexedPages

    def foo(self):
        return # foo is doing just nothing

        


class IndexPage(object):
    '''
    The IndexPage is the main page, which gets called, if you open your Browser at localhost:8080.
    It sets the routeNames for all other pages
    '''

    start = StartPage() # StartPage() ist available under localhost:8080/start/
    indexed_pages = ShowIndexedPages() # ShowIndexedPages() ist available under localhost:8080/indexed_pages/

    def index(self):
        '''
        Provides a HTML Template, which links to Start and ShowIndexed Page
        '''
        return '''<!doctype html>
<html lang="en" ng-app="app">
<head>
  <meta charset="UTF-8">
  <title>SearchSpiegel</title>
  <script src="https://code.jquery.com/jquery.js"></script>
  <link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css">
  <script src="//netdna.bootstrapcdn.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>
</head>
<body>
<div class="container">
<br/>
<a href="/start/">Suche aufrufen</a> |
<a href="/index_start/">Indexierungs-Thread aufrufen</a>
</div>
</body>'''
    index.exposed = True # necessary so this page/function can be visited



# Inits the WebServer with the IndexPage
cherrypy.quickstart(IndexPage())






