import logging
import pprint
import sys

from BingApi import BingApi
import Result

class Binger():
    def __init__(self):
        self.queryWords = ['Gates']
        self.targetPrecision = 0.8
        self.b = BingApi()
        self.iterations = 0
        self.results = []
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        self.getInitParameteres()
    
    def getInitParameteres(self):
        for i in range(10):
            try:
                print ('Query Words'+" "*15)[:15],':',
                readWords = sys.stdin.readline()
                if(len(readWords)):
                    self.queryWords = readWords.split(" ")
                    break
            except:
                pass
        for i in range(10):
            try:
                print ('Target Precision'+" "*15)[:15],':',
                self.targetPrecision = float(sys.stdin.readline())
                break
            except:
                pass
        print self.queryWords
        print self.targetPrecision
        return
    
    def getRelevance(self):
        self.relevance = []
        for res in self.results:
            Result.printResult(res)
            print 'Relevance {0,1}',':',
            rel = 10
            for i in range(10):
                try :
                    print ('relevance {0,1}:'+" "*15)[:15],':',
                    rel = int(sys.stdin.readline())
                    print
                except :
                    pass
            print "\n"
            self.relevance.append(rel)
        return
    
    def getCurrentPrecision(self):
        return 1.0*sum(self.relevance)/len(self.relevance)
    
    def getNextIteration(self):
        self.results = self.b.search('+'.join(self.queryWords))
        self.getRelevance()
        self.logger.info('Current relevance / target relevance : %f / %f', self.getCurrentPrecision(), self.targetPrecision)
        return (self.getCurrentPrecision() >= self.targetPrecision)
