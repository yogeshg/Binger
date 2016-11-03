from Topic import Topic
from subprocess import check_output

class ContentSummaryConstructor(object):
    def __init__(self, root, host):
        self.host = host
        self.root = root

    def pageToWords(self, page):
        parsed_page = ""
        references_index = page.find(Web.References)
        is_in_brackets = False
        is_space_already = False
        for i in xrange(references_index):
            char = page[i].lower()
            if not is_in_brackets:
                if char.isalpha():
                    parsed_page += char
                    is_space_already = False
                else:
                    if char == '[':
                        is_in_brackets = True
                    if not is_space_already:
                        parsed_page += ' '
                        is_space_already = True
            else:
                if char == ']':
                    is_in_brackets = False
        return set(parsed_page.split())

    def grabWordsFromURLs(self, url):
    	#transfer URL to text
    	if((url[-4:] == ".pdf" or url[-4:] == ".ppt" or url[-5:] == ".doc" or url[-5:] == ".pptx" or url[-5:] == ".docx")):
			continue
		try:
			page_output = check_output("lynx --dump " + url, shell=True)
		except Exception as e:
			print e
			print "Error occured, pass\n\n"


	def ContentSummaryConstruct(self):
		#traversal each topic(node) in the tree. If the sampleCD of this node is not empty, generate summary for this node.


		
	            
if __name__ == "__main__":
    r = Topic("Root")
    csc = ContentSummaryConstructor(r, "google.com")
    