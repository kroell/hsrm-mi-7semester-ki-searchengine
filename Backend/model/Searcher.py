import lucene

class Searcher(object):

    def __init__(self, indexer):
        self.parser = lucene.MultiFieldQueryParser(
            lucene.Version.LUCENE_CURRENT,
            ["content"],
            indexer.analyzer)
        self.searcher = lucene.IndexSearcher(indexer.store, readOnly=True)
        self.indexer = indexer


    def search(self, queryString):
        query = self.parser.parse(self.parser, queryString)
        scoredocs = self.searcher.search(query, 50).scoreDocs
        for i, scoredoc in enumerate(scoredocs):
            d = self.searcher.doc(scoredoc.doc)            
            print unicode(d.getField("url"))
    
