from collections import defaultdict

from BingApi import BingApi
from Topic import Topic

import logging
logging.basicConfig( level=logging.INFO )

class QProber(object):

    def __init__(self):
        self.bing = BingApi()
        self.r = Topic("Root")
        self.r.load()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(self.__class__.__name__+'Initialised')
        return

    def probe(self, host, ts, tc):
        print "Classifying..."
        self.host = host
        self.topic_coverage = defaultdict(float)
        self.topic_specificity = defaultdict(float)
        self.result = []
        self.result.append(self.r)
        self.classify(self.r, ts, tc, 1.0)
        print "Result of Classifying:"
        for each in self.result:
        	#print each.name
        	if(len(each.subtopics)==0):
        		print host+":" + self.printPath(each.name)
        	else:
        		tmp = 0
        		for eachsub in each.subtopics:
        			if each.subtopics.get(eachsub) in self.result:
        				tmp = 1
        		if(tmp==0):
        			print host+":" + self.printPath(each.name)
        #print self.r.sampleCD

    
    def classify(self, topic, ts, tc, src_topic_espec):
        self.logger.info('classifying %s, %f, %d', topic.name, ts, tc)
        #Calculate coverage info
        for query in topic.queries:
        	subtopic = topic.queries.get(query)
        	subtopicobject = topic.subtopics.get(subtopic)
        	self.topic_coverage[subtopic] = self.topic_coverage[subtopic] + self.bing.searchSiteMatch(self.host, query, subtopicobject)
        totalCount = 0
        for subtopic in topic.subtopics:
        	totalCount += self.topic_coverage[subtopic]
        	#print self.topic_coverage[subtopic]
        #print totalCount

        #Calculate specificity info
        for subtopic in topic.subtopics:
            self.topic_specificity[subtopic] = (src_topic_espec * self.topic_coverage[subtopic] / totalCount)

        #Judge result
        for subtopic in topic.subtopics:
        	if(self.topic_specificity[subtopic] >= ts and self.topic_coverage[subtopic] >= tc):
				self.result.append(topic.subtopics.get(subtopic))
				if(topic.name==self.r.name):
					self.classify(topic.subtopics.get(subtopic), ts, tc, self.topic_specificity[subtopic])

    
    def printPath(self, name):
        path = "Root"
    	if name in self.r.subtopics:
    		path = path + "/" +name
    	elif name!="Root":
    		for subtopic in self.r.subtopics:
    			subtopicobject = self.r.subtopics.get(subtopic)
    			if subtopic == name:
    				path = path+"/"+name
    			elif name in subtopicobject.subtopics:
    				path = path + "/" + subtopicobject.name + "/" + name
    	return path



    
if __name__ == "__main__":
    
    qp = QProber()
    qp.probe("health.com",0.6, 100)
    qp = QProber()
    qp.probe("fifa.com",0.6, 100)
    qp = QProber()
    qp.probe("diabetes.org",0.6, 100)
    qp = QProber()
    qp.probe("hardwarecentral.com",0.6, 100)
    qp = QProber()
    qp.probe("yahoo.com",0.6, 100)
    print qp.r
    
