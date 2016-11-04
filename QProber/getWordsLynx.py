import os
import re

import logging
from collections import Counter

from Util import FileDict, DirDict

IGNORE_LINES_AFTER = 'References'
IGNORE_PATTERN = re.compile(r'\[.*?\]')
WORD_PATTERN = re.compile(r'[A-Za-z]+')

class lynxHelper():
    def __init__(self):
        self.cache = DirDict('cache.lynx')
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(self.__class__.__name__+'Initialised')
        return
    
    def run(self, url):
        '''
        param: url: string
        returns: filepointer: use readline or readlines
        '''
        if( not self.cache.has_key(url) ):
            self.logger.info('lynx-ing... %s', url)
            self.cache[url] = os.popen('lynx -dump {url}'.format(url=url))
        else :
            self.logger.debug('using cached... %s', url)
        return self.cache[url]

def getCountset(lines):
    text = ''
    countset = Counter()
    for l in lines:
        if l.startswith(IGNORE_LINES_AFTER):
            break
        else :
            l = IGNORE_PATTERN.sub('', l)
            words = WORD_PATTERN.findall(l)
            for w in words:
                countset[w.lower()]+=1
    return countset

if __name__ == '__main__':
    url = 'www.google.com'
    try:
        url = sys.argv[1]
    except:
        pass
    lynx = lynxHelper()
    f = lynx.run(url)
    c = getCountset(f.split("\n"))
    print c
    for w in sorted(c.iterkeys()):
        print w,
    pass
