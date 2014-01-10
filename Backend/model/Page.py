'''
Created on 06.12.2013

@author: soerenkroell
'''

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
    

