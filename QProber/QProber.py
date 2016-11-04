from collections import defaultdict, Counter

import logging
logging.basicConfig( level=logging.INFO )

from BingApi import BingApi
from Topic import Topic
from getWordsLynx import LynxHelper, getCountset

class QProber(object):

    def __init__(self, bingApiKey=None):
        self.bing = BingApi(api=bingApiKey)
        self.r = Topic("Root")
        self.r.load()
        self.lynx = LynxHelper()
        self.webResultsCounter = Counter()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(self.__class__.__name__+'Initialised')
        return

    def probe(self, host, ts, tc):
        print "Classifying...", host
        self.host = host
        self.topic_coverage = defaultdict(float)
        self.topic_specificity = defaultdict(float)
        self.result = []
        self.result.append(self.r)
        self.classify(self.r, ts, tc, 1.0)
        for each in self.result:
        	#print each.name
        	if(len(each.subtopics)==0):
        		print host, "belongs to topic", self.printPath(each.name)
        	else:
        		tmp = 0
        		for eachsub in each.subtopics:
        			if each.subtopics.get(eachsub) in self.result:
        				tmp = 1
        		if(tmp==0):
        			print host, "belongs to topic", self.printPath(each.name)
        #print self.r.sampleCD

    
    def classify(self, topic, ts, tc, src_topic_espec):
        self.logger.info('classifying %s, %f, %d', topic.name, ts, tc)
        #Calculate coverage info
        for query in topic.queries:
        	subtopic = topic.queries.get(query)
        	subtopicobject = topic.subtopics.get(subtopic)
        	totalWebResults = self.bing.searchSiteMatch(self.host, query, subtopicobject)
        	self.webResultsCounter[topic.name, self.host, query] += totalWebResults
        	self.topic_coverage[subtopic] = self.topic_coverage[subtopic] + totalWebResults
        totalCount = 0
        for subtopic in topic.subtopics:
        	totalCount += self.topic_coverage[subtopic]
        	#print self.topic_coverage[subtopic]
        #print totalCount

        #Calculate specificity info
        try:
            for subtopic in topic.subtopics:
                self.topic_specificity[subtopic] = (src_topic_espec * self.topic_coverage[subtopic] / totalCount)
                print 'for', subtopic, 'specificity=', self.topic_specificity[subtopic], 'coverage=', self.topic_coverage[subtopic]
        except:
            # error due to math
            pass

        #Judge result
        for subtopic in topic.subtopics:
        	if(self.topic_specificity[subtopic] >= ts and self.topic_coverage[subtopic] >= tc):
				self.result.append(topic.subtopics.get(subtopic))
				if(topic.name==self.r.name):
					self.classify(topic.subtopics.get(subtopic), ts, tc, self.topic_specificity[subtopic])

    def getContentSummary(self, node, host):
            # for (host, urls) in qp.r.sampleCD.iteritems():
            urls = node.sampleCD[host]
            countset = Counter()
            for url in urls:
                lines = self.lynx.run(url).split('\n')
                countset += getCountset(lines)
            self.logger.info( "num words in %s, %s %d", node.name, host, len(countset))
            s = []
            for w in sorted(set(countset.keys()).union(set(node.queries.keys()))):
                webResults = self.webResultsCounter[node.name, host, w]
                if(webResults < 0):
                    webResults = -1
                line = "#".join([ w, str(float(countset[w])), str(float(webResults)) ])
                s.append( line+"\n" )
            return s
 
    def writeContentSummaries(self, host):
        for node in [self.r]+list(self.r.iterSubtopics()):
          try:
            cs = self.getContentSummary( node, host )
            filename = '{}-{}.txt'.format(node.name, host)
            with open( filename, 'w' ) as f:
                f.writelines(cs)
            print filename, 'generated.'
          except:
            pass

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
    for host in ["health.com", "fifa.com"]:
        qp.probe(host, 0.6, 100)
        qp.writeContentSummaries(host)
    qp.probe("diabetes.org",0.6, 100)
    qp.probe("hardwarecentral.com",0.6, 100)
    qp.probe("yahoo.com",0.6, 100)

