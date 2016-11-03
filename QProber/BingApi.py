import logging

import urllib2
handler=urllib2.HTTPHandler(debuglevel=1)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)

import urllib2

import base64

import json

import pprint

import Result

class BingApi():
    def __init__(self, api=None):
        if( api==None ):
            with open('APIKEY.txt', 'r') as f:
                api = f.readline().strip()
        accountKey = api
        accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
        self.headers = {'Authorization': 'Basic ' + accountKeyEnc}
        self.url_format = 'https://api.datamarket.azure.com/Data.ashx/Bing/SearchWeb/v1/Composite?Query=%27site%3a{site}%20{query_word}%27&$top={num_results}&$format={output_format}'
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(self.__class__.__name__+'Initialised')
        self.cache = {}
    
    def searchSite(self, site, query_word, num_results=10, output_format='json'):
        query = self.url_format.format(site=site, query_word=query_word, num_results=num_results, output_format=output_format)
        
        self.logger.info(("searching...\n\t"+query))
        
        if(not self.cache.has_key(query)):
            req = urllib2.Request(query, headers = self.headers)
            self.logger.info('Did not find in cache, requesting...\n\t'+req.get_full_url())
            url_response = urllib2.urlopen(req)
            json_response = json.load(url_response)
            self.cache[query] = Result.parseCompositeResult(json_response['d']['results'][0], num_results=num_results)
        
        # returns a dictionary with keys Web and Webtotal
        # web - a list of results
        # webtotal - number of results
        return self.cache[query]

    def searchSiteMatch(self, host, query, topic):
        query = query.replace(' ', "%20")
        bing_url_Prefix = "https://api.datamarket.azure.com/Data.ashx/Bing/SearchWeb/v1/Composite?Query="
        bing_url = bing_url_Prefix + "%27site%3a" + host + "%20" + query +"%27&$top=10&$format=json"

        #Send request to Bing Search
        request = urllib2.Request(bing_url, headers=self.headers)
        response = urllib2.urlopen(request)
        
        #Get and analyze result
        content = json.load(response)
        count = float(content["d"]["results"][0]["WebTotal"])
        webs = content["d"]["results"][0]["Web"]
        urls = set()
        for i in xrange(len(webs)):
            if i == 4:
                break
            topic.addDocumentToThisAndParents(host,webs[i]["Url"])

        
        #print count
        return count


if __name__ == "__main__":
    b = BingApi()
    r = b.searchSite('fifa.com', 'messi', num_results=1)
    # print bing.searchSiteMatch("yahoo.com", "hello World")

