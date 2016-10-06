
# coding: utf-8

# In[1]:
from QueryExpander import QueryExpander
import logging
from Binger import Binger


# In[2]:

logging.basicConfig(level=logging.DEBUG)
app = Binger()

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


