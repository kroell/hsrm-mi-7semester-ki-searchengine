import lucene                    

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


        
