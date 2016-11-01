import logging
logger = logging.getLogger(__name__)

class Topic():
    def __init__(self, topic):
        self.name = topic
        self.subtopics={}
        self.queries={}
        return

    def load(self):
        logger.debug('loading... '+str(self))
        try:
            with open('./data/'+self.name.lower()+'.txt','r') as f:
              for line in f:
                (subtopic, query) = line.strip().split(' ',1)
                if( not self.subtopics.has_key(subtopic) ):
                    self.subtopics[subtopic] = Topic(subtopic)
                self.queries[query] = subtopic
        except Exception as e:
            logger.exception(e)
            logger.debug('leaf node encountered')
        for s in self.subtopics.itervalues():
            s.load()
        return

    def str(self, pre):
        s = "{}{} : {} queries".format(pre, self.name, str(len(self.queries)))
        for sub in self.subtopics.itervalues():
            s+='\n'+sub.str(pre+'  ')
        return s 
    
    def __str__(self):
        return self.str('')

