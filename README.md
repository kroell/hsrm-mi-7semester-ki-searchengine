hsrm-mi-7semester-ki-searchengine
=================================

Um die SearchEngine verwenden zu können müssen folgende Python Pakete installiert sein:  

BeautifulSoup installieren  
http://www.crummy.com/software/BeautifulSoup/bs4/download/4.3/

NLTK installieren  
http://nltk.org/install.html

PyLucene installieren  
http://lucene.apache.org/pylucene/install.html

PyLucene Makefile für Mac  
https://gist.github.com/peplin/728598

ANT installieren  
http://superuser.com/questions/610157/how-do-i-install-ant-on-os-x-mavericks
  
<br/>

<p>Zum Start des Webservers <b>python WebServer.py</b> ausführen. Dieser läuft dann unter localhost:8080. Im Pfad <b>localhost:8080/start/</b> können Suchanfragen gestellt werden. <b>localhost:8080/start/search</b> zeigt die Suchergebnisse. </p>
<p><b>localhost:8080/indexed_pages/</b> zeigt die Anzahl und URLs der indizierten Seiten.</p>

<br/>

<b>Ansicht der Suchresultate</b>
<img src="http://www.idseven.info/github/search-spiegel-result.png"> </img>

<br/>

<b>Ansicht der indexierten Seiten</b>
<img src="http://www.idseven.info/github/search-spiegel-index.png"> </img>


<br/>

MIT Licence
=================================
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
