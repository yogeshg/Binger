
RESULT_KEYS = ['Title','Url','Description']

def printResult(res):
    for k in RESULT_KEYS:
        print (k+" "*15)[:15],':',res[k]

