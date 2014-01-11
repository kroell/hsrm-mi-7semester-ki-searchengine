# -*- encoding: UTF-8 -*-
import os

import cherrypy
import SearchEngine as searchEngine


class StartPage(object):
    def index(self):
        return self.template()
    index.exposed = True

    def doSearch(self, suche=None):
        URL = 'http://www.spiegel.de/'
        spider = searchEngine.Spider(URL)
        spider.initSpider(URL)
        spider.preparePage()
        indexer = searchEngine.Indexer()    
        [indexer.addPage(p) for p in spider.pages.values()] 
        indexer.close()
        searcher = searchEngine.Searcher(indexer)
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
            <p class="lead">Alles was du schon immer auf Spiegel.de finden wolltest, findest du hier.</p>
      </div>
      <div>
      <form class="form-inline" role="form" method="post" action="doSearch">
              <div class="col-md-10">
                <input type="text" class="form-control input-lg" id="suchanfrageInput" name="suche" placeholder="Deine Suchanfrage" required>
              </div>
              
              <button type="submit" class="btn btn-primary btn-lg">Abschicken</button>
      </form>
      </div>
      <div id="answer" class="col-md-12"><br/>
%s
      </div>
</div>
</body>''') % searcher.search(suche)
    doSearch.exposed = True

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
            <p class="lead">Alles was du schon immer auf Spiegel.de finden wolltest, findest du hier.</p>
      </div>
      <div class="searchBar">

      <form class="form-inline" role="form" method="post" action="doSearch">

              <div class="col-md-10">
                <input type="text" class="form-control input-lg" id="suchanfrageInput" name="suche" placeholder="Deine Suchanfrage" required>
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

      


class IndexPage(object):
    start = StartPage()

    def index(self):
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
<a href="/start/">Suche aufrufen</a>
</body>'''
    index.exposed = True





cherrypy.quickstart(IndexPage())
