import sys
import base64
import urllib2
import json
from urlparse import urlparse
import re
import math


class QueryExpander(object):
  def __init__(self):
    self.a = 1.0
    self.b = 0.8
    self.c = -0.1
    self.query_words = []
    self.all_words = []
    self.idf_list = []
    self.tf_matrix = []
    self.tfidf_matrix = []
    self.totalscore = []
    self.stop_words = ["I","me","my","myself","we","us","our","ours","ourselves","you","your","yours",
                "yourself","yourselves","he","him","his","himself","she","her","hers","herself","it","its",
                "itself","they","them","their","theirs","themselves","what","which","who","whom","whose",
                "this","that","these","those","am","is","are","was","were","be","been","being","have","has",
                "had","having","do","does","did","doing","will","would","should","can","could","ought",
                "i'm","you're","he's","she's","it's","we're","they're","i've","you've","we've","they've",
                "i'd","you'd","he'd","she'd","we'd","they'd","i'll","you'll","he'll","she'll","we'll","they'll",
                "isn't","aren't","wasn't","weren't","hasn't","haven't","hadn't","doesn't","don't","didn't",
                "won't","wouldn't","shan't","shouldn't","can't","cannot","couldn't","mustn't","let's","that's",
                "who's","what's","here's","there's","when's","where's","why's","how's","a","an","the","and",
                "but","if","or","because","as","until","while","of","at","by","for","with","about","against",
                "between","into","through","during","before","after","above","below","to","from","up","upon",
                "down","in","out","on","off","over","under","again","further","then","once","here","there",
                "when","where","why","how","all","any","both","each","few","more","most","other","some",
                "such","no","nor","not","only","own","same","so","than","too","very","say","says","said",
                "shall","a","s","ve","lets","days","ago"]
  
  def get_tf(self, all_results):
    tf_matrix = [[0 for col in range(len(self.all_words))] for row in range(len(all_results))]
    #print tf_matrix
    for i, result in enumerate(all_results):
      url = result.get('Url')
      urlinfo = re.findall('\w+',url)
      urlinfo = " ".join(urlinfo)
      infoList = [ result.get('Title'), urlinfo, result.get('Description') ]
      longString = " ".join(infoList)
      re.sub(r'[^\x00-\x7F]+', ' ', longString)
      ori_words = longString.split(" ")
      ori_words = [x.lower() for x in ori_words]
      ori_words = [re.sub('[^a-zA-Z0-9 \n\.]', '', x) for x in ori_words]
      for j, word in enumerate(self.all_words):
        tf_matrix[i][j] = 1.0 * ori_words.count(word)/len(ori_words)
    return tf_matrix


  


  def get_idf(self, all_results):
    total_results = float(len(all_results))
    idf_list = [0.0] * len(self.all_words)
    #print all_results
    for result in all_results:
      url = result.get('Url')
      urlinfo = re.findall('\w+',url)
      urlinfo = " ".join(urlinfo)
      infoList = [ result.get('Title'), urlinfo, result.get('Description') ]
      longString = " ".join(infoList)
      re.sub(r'[^\x00-\x7F]+', ' ', longString)
      ori_words = longString.split(" ")
      ori_words = [x.lower() for x in ori_words]
      ori_words = [re.sub('[^a-zA-Z0-9 \n\.]', '', x) for x in ori_words]
      for index, word in enumerate(self.all_words):
        #print word
        #print ori_words
        if word in ori_words:
          idf_list[index] += 1.0
    #print idf_list
    for i in xrange(len(idf_list)):
      idf_list[i] = math.log(total_results / idf_list[i])
    #print idf_list
    idf_list
    self.idf_list=idf_list


  
  def getAllWords(self, query, all_results):
    self.query_words = query.split(" ")
    self.query_words = [x.lower() for x in self.query_words]
    #print self.query_words
    for result in all_results:
      url = result.get('Url')
      urlinfo = re.findall('\w+',url)
      urlinfo = " ".join(urlinfo)
      infoList = [ result.get('Title'), urlinfo, result.get('Description') ]
      longString = " ".join(infoList)
      re.sub(r'[^\x00-\x7F]+', ' ', longString)
      words = longString.split(" ")
      for word in words:
        word = word.lower()
        word = re.sub('[^a-zA-Z0-9 \n\.]', '', word)
        if(word in self.stop_words or word in self.query_words or word in self.all_words):
          continue
        else:
          self.all_words.append(word)
    #print self.all_words
    #print all_results

  def generate_tfidf(self, tf_matrix, idf_list, all_results):
    self.tfidf_matrix = tf_matrix = [[0 for col in range(len(self.all_words))] for row in range(len(all_results))]
    idf = 0.0
    for j, word in enumerate(self.all_words):
      idf = idf_list[j]
      for i, each in enumerate(all_results):
        tf=self.tf_matrix[i][j]
        self.tfidf_matrix[i][j] = (self.tf_matrix[i][j] * idf)
    #print self.tf_matrix
    #print self.idf_list
    #print self.tfidf_matrix

  def calculate_Weight(self, query, all_results, yes_no):
    self.getAllWords(query, all_results)
    self.get_idf(all_results)
    relevant = 0
    nonrelevant = 0
    for each in yes_no:
      if(each==1):
        relevant = relevant + 1
      else:
        nonrelevant = nonrelevant + 1
    if(relevant==0):
      relevant=1
    elif(nonrelevant == 0):
      nonrelevant=1
    #Create two list (R and NR)
    r_results = []
    nr_results = []
    for i, each in enumerate(yes_no):
      if(each==1):
        r_results.append(all_results[i])
      else:
        nr_results.append(all_results[i])
    #print r_results
    #print nr_results
    self.tf_matrix = self.get_tf(all_results)
    #print self.tf_matrix

    self.generate_tfidf(self.tf_matrix, self.idf_list, all_results)
    #print self.tfidf_matrix

    for i, each in enumerate(yes_no):
      for j, word in enumerate(self.all_words):
        tmp = self.tfidf_matrix[i][j]
        if each==1:
          self.tfidf_matrix[i][j] = tmp * self.b
        else:
          self.tfidf_matrix[i][j] = tmp * self.c
        #print self.tfidf_matrix[i][j]
    #print self.tfidf_matrix

    self.totalscore = range(len(self.all_words))
    for j, word in enumerate(self.all_words):
      self.totalscore[j]=0
      for i, each in enumerate(yes_no):
        tmp = self.totalscore[j]
        self.totalscore[j] = tmp + self.tfidf_matrix[i][j]
    #print self.totalscore

    index = self.totalscore.index(max(self.totalscore))
    print "The new query is: "
    print query + " " + self.all_words[index]
    return query + " " + self.all_words[index]

