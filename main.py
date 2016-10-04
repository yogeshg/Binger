
# coding: utf-8

# In[1]:

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
        print app.queryWords
        print app.results
        print app.relevance

        # Call the query modifier here app.queryWords = f(app.queryWords, app.results, app.relevance)
        app.queryWords = ['Gates', 'Bill']


