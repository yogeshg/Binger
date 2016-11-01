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
        
        if(not self.cache.has_key(query_word)):
            req = urllib2.Request(query, headers = self.headers)
            self.logger.info('Did not find in cache, requesting...\n\t'+req.get_full_url())
            url_response = urllib2.urlopen(req)
            json_response = json.load(url_response)
            # contents = []
            # for i in range(10):
            #     contents.append({k:json_response['d']['results']['Web'][i][k].encode('ascii','ignore') for k in Result.RESULT_KEYS})
            self.cache[query_word] = Result.parseCompositeResult(json_response['d']['results'][0])
        
        return self.cache[query_word]

