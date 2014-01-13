# -*- encoding: UTF-8 -*-
import os

import thread
import cherrypy
import SearchEngine as engine

import cherrypy.process.plugins

import BackgroundTaskQueue


URL = 'http://www.spiegel.de/'
searchEngine = engine.SearchEngine(URL)
indexer = None

class StartPage(object):
    def index(self):
        wd = cherrypy.process.plugins.BackgroundTask(20,self.indexThread) # ruft alle 5 Sekunden self.func auf
        wd.start()
        print "Thread-Monster wurde gestartet..."
        return self.template()
        wd.cancel()

        #wd.cancel()
    index.exposed = True

    def search(self, query=None):
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
      <!--<form class="form-inline" role="form" method="post" action="search">
              <div class="col-md-10">
                <input type="text" class="form-control input-lg" id="queryInput" name="query" placeholder="Deine Suchanfrage" required>
              </div>
              
              <button type="submit" class="btn btn-primary btn-lg">Abschicken</button>
      </form>-->

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
    search.exposed = True

    def template(self):
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
        searchEngine.startSpiderAndIndex()
        




class ShowIndexedPages(object):
    def index(self):
        indexedPages = searchEngine.getIndexedPages()
        return self.template(indexedPages)
    index.exposed = True

    def template(self, indexedPages):
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


class IndexStartPage(object):
    def index(self):
        wd = cherrypy.process.plugins.BackgroundTask(20,self.indexThread) # ruft alle 5 Sekunden self.func auf
        wd.start()

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
<p>Indexierungs-Thread wurde im Hintergrund gestart...</p>
</div>
</body>'''

        wd.cancel()
    index.exposed = True

    def indexThread(self):
        searchEngine.startSpiderAndIndex()
        


class IndexPage(object):
    start = StartPage()
    indexed_pages = ShowIndexedPages()
    index_start = IndexStartPage()

    def index(self):
        #bgtask.put(log, "index was called", ip=cherrypy.request.remote.ip))
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
    index.exposed = True




cherrypy.quickstart(IndexPage())






