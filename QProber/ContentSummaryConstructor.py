from Topic import Topic
from subprocess import check_output
import getWordsLynx
import os
import re
from collections import Counter

class ContentSummaryConstructor(object):
    def __init__(self, root, host):
        self.host = host
        self.root = root
        self.IGNORE_LINES_AFTER = 'References'
        self.IGNORE_PATTERN = re.compile(r'\[.*?\]')
        self.WORD_PATTERN = re.compile(r'[A-Za-z]+')

    def runLynx(self, url):
        '''
        param: url: string
        returns: filepointer: use readline or readlines
        '''
        return os.popen('lynx -dump {url}'.format(url=url))

    def preProcess(self, lines):
        text = ''
        countset = Counter()
        for l in lines:
            if l.startswith(self.IGNORE_LINES_AFTER):
                break
            else :
                l = self.IGNORE_PATTERN.sub('', l)
                words = self.WORD_PATTERN.findall(l)
                for w in words:
                    countset[w.lower()]+=1
                #print countset
        return countset

    def ContentSummaryConstruct(self):
        #traversal each topic(node) in the tree. If the sampleCD of this node is not empty, generate summary for this node.
        rootset = r.sampleCD().get(hostname)
        for url in rootset:
	        #Get a set of word for this url
		#Now we have many sets of words (one set for one URL) and we could get doc frequency
		#Write doc frequency info to txt files

		#Check each subtopic, if the subtopic's sampleCD is not empty do the same thing above


		#Remember！！！
		#We have to generate txt file for root node 
		#And we might need to generate file for second level nodes (like health, sport) if the sampleCD is not empty.
		#We never generate text file for leaf.


	            
if __name__ == "__main__":
    hostname = "www.google.com"
    r = Topic("Root")
    r.load()
    r.addDocumentToThisAndParents(hostname, "health.com")
    r.addDocumentToThisAndParents(hostname, "yahoo.com")
    csc = ContentSummaryConstructor(r, hostname)
    csc.ContentSummaryConstruct()
    