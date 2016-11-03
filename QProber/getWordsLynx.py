import os
import re

from collections import Counter

def runLynx(url):
    '''
    param: url: string
    returns: filepointer: use readline or readlines
    '''
    return os.popen('lynx -dump {url}'.format(url=url))

IGNORE_LINES_AFTER = 'References'
IGNORE_PATTERN = re.compile(r'\[.*?\]')
WORD_PATTERN = re.compile(r'[A-Za-z]+')

def preProcess(lines):
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
            #print countset
    return countset

if __name__ == '__main__':
    url = 'www.google.com'
    try:
        url = sys.argv[1]
    except:
        pass
    f = runLynx('www.google.com')
    c = preProcess(f)
    for w in sorted(c.iterkeys()):
        print w

