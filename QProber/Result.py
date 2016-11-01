
RESULT_KEYS = ['Title','Url','Description']

def printResult(res):
    for k in RESULT_KEYS:
        print (k+" "*15)[:15],':',res[k]

def parseWebResults(web_json_list, num_results=10):
    contents = []
    for i in range(num_results):
        contents.append({k:web_json_list[i][k].encode('ascii','ignore') for k in RESULT_KEYS})
    return contents 

def parseCompositeResult(result_json_dict, num_results=10):
    return {'WebTotal': result_json_dict['WebTotal'], 'Web':parseWebResults(result_json_dict['Web'], num_results)} 
 
