from collections import defaultdict
import logging

class Topic():
    def __init__(self, topic):
        self.name = topic
        self.subtopics={}
        self.queries={}
        self.parent=None
        # db:str -> docs:set
        # r.sampleCD['fifa.com']
        self.sampleCD=defaultdict(set)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(self.__class__.__name__+'Initialised')
        return

    def load(self, parent=None):
        self.parent = parent
        self.logger.debug('loading... '+str(self))
        try:
            with open('./data/'+self.name.lower()+'.txt','r') as f:
              for line in f:
                (subtopic, query) = line.strip().split(' ',1)
                if( not self.subtopics.has_key(subtopic) ):
                    self.subtopics[subtopic] = Topic(subtopic)
                self.queries[query] = subtopic
        except Exception as e:
            # self.logger.exception(e)
            self.logger.debug('leaf node encountered')
        for s in self.subtopics.itervalues():
            s.load( parent=self )
        return

    def iterSubtopics(self):
        return self.subtopics.itervalues()

    def addDocumentToThisAndParents(self, database, document):
        self.sampleCD[database].add(document)
        if(self.parent):
            return self.parent.addDocumentToThisAndParents(database, document)
        else:
            return

    def str(self, pre):
        s = "{}{} : {} queries".format(pre, self.name, str(len(self.queries)))
        for sub in self.iterSubtopics():
            s+='\n'+sub.str(pre+'  ')
        return s 
    
    def __str__(self):
        return self.str('')

if __name__ == "__main__":
    r = Topic("Root")
    r.load()
    print r

    for subtopic in r.iterSubtopics():
        print subtopic.subtopics
        print subtopic.queries

    print r.subtopics["Computers"].queries

    print r.name, r.sampleCD
    for s in r.iterSubtopics():
        print s.name, s.sampleCD

    s.addDocumentToThisAndParents('fifa.com', 'YOU CAN ADD ANY OBJECT HERE')
    s.addDocumentToThisAndParents('fifa.com', 'Test')
    s.addDocumentToThisAndParents('fifa.com', 'YOU CAN ADD ANY OBJECT HERE')

    print r.name, r.sampleCD
    for s in r.iterSubtopics():
        print s.name, s.sampleCD

