#! /usr/bin/python2.7

from QueryExpander import QueryExpander
import logging
from Binger import Binger
import sys
import argparse


def main():

    p = argparse.ArgumentParser(__doc__)
    p.add_argument('apikey', type=str, help='Bing api key')
    p.add_argument('query', type=str, help='Type quote enclosed query here')
    p.add_argument('precision10', type=float, help='Target precision at 10')
    a = p.parse_args()

    logging.basicConfig(level=logging.DEBUG)
    logging.debug(str(a.__dict__))
    app = Binger(a.apikey, a.query.split(), a.precision10)
    
    maxIterations = 10
    
    for i in range(maxIterations):
        success = app.getNextIteration()
        print success
        if(success):
            print 'Success!!'
            break
        else:
            app.queryWords = ' '.join(app.queryWords)
            print app.queryWords
            print app.results
            print app.relevance
            abc = QueryExpander()
            app.queryWords = abc.calculate_Weight(app.queryWords, app.results, app.relevance)
            app.queryWords = app.queryWords.split(' ')

if __name__ =='__main__' :
    main()

