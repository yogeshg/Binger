from Topic import Topic
from subprocess import check_output

class ContentSummaryConstructor(object):
    def __init__(self, root, host):
        self.host = host
        self.root = root

    def pageToWords(self, page):
        #Parse page to a set of words




        

    def grabWordsFromURLs(self, url):
    	#transfer URL to text
    	if((url[-4:] == ".pdf" or url[-4:] == ".ppt" or url[-5:] == ".doc" or url[-5:] == ".pptx" or url[-5:] == ".docx")):
			#When it's not a webpage
			return set()
		try:
			page_output = check_output("lynx --dump " + url, shell=True)
			return self.pageToWords(page_output)

		except Exception as e:
			print e
			print "Error occured, pass\n\n"
			return set()


	def ContentSummaryConstruct(self):
		#traversal each topic(node) in the tree. If the sampleCD of this node is not empty, generate summary for this node.


		
	            
if __name__ == "__main__":
    r = Topic("Root")
    csc = ContentSummaryConstructor(r, "google.com")
    