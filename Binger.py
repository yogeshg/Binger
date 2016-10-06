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
        self.getInitParameteres()
    
    def getInitParameteres(self):
        for i in range(10):
            try:
                print ('Query Words'+" "*16)[:16],':',
                readWords = sys.stdin.readline().strip()
                if(len(readWords)):
                    self.queryWords = readWords.split(" ")
                    break
            except Exception as e:
                print 'Error while reading Query words:', e
        for i in range(10):
            try:
                print
                print ('Target Precision'+" "*16)[:16],':',
                self.targetPrecision = float(sys.stdin.readline().strip())
                break
            except Exception as e:
                print 'Error while reading Query words:', e
        self.logger.info( 'Starting Bing improvement with' + str(self.queryWords) + str(self.targetPrecision) )
        return
    
    def getRelevance(self):
        self.relevance = []
        for res in self.results:
            Result.printResult(res)
            rel = 10
            for i in range(10):
                try :
                    print ('relevance {0,1}'+" "*16)[:16],':',
                    rel = int(sys.stdin.readline())
                    break
                except Exception as e:
                    print 'Error while reading Query words:', e
            self.relevance.append(rel)
        return
    
    def getCurrentPrecision(self):
        return 1.0*sum(self.relevance)/len(self.relevance)
    
    def getNextIteration(self):
        self.results = self.b.search('+'.join(self.queryWords))
        self.getRelevance()
        self.logger.info('Current relevance / target relevance : %f / %f', self.getCurrentPrecision(), self.targetPrecision)
        return ((self.getCurrentPrecision() >= self.targetPrecision) or (self.getCurrentPrecision() <= 0))



