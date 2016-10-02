import logging

import urllib2

import base64

import json

import pprint

import Result

class BingApi():
    def __init__(self):
        accountKey = 'QCFuIkEuEvdAkzCnFJSC732Oar52QRjlfFaCS1LCSWc'
        accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
        self.headers = {'Authorization': 'Basic ' + accountKeyEnc}
        self.url_format = 'https://api.datamarket.azure.com/Bing/Search/Web?Query=%27{query_word}%27&$top={num_results}&$format={output_format}'
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        self.cache = {}
    
    def search(self, query_word, num_results=10, output_format='json'):
        query = self.url_format.format(query_word=query_word, num_results=num_results, output_format=output_format)
        
        self.logger.info(("searching...\n\t"+query))
        
        if(not self.cache.has_key(query_word)):
            req = urllib2.Request(query, headers = self.headers)
            self.logger.info('Did not find in cache, requesting...\n\t'+req.get_full_url())
            url_response = urllib2.urlopen(req)
            json_response = json.load(url_response)
            contents = []
            for i in range(10):
                contents.append({k:json_response['d']['results'][i][k] for k in Result.RESULT_KEYS})
            self.cache[query_word] = contents
        
        return self.cache[query_word]

