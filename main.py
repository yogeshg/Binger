
# coding: utf-8

# In[1]:

from Binger import Binger


# In[2]:

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

        app.queryWords = ['Gates', 'Bill']


