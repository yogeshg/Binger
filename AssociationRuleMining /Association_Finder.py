from operator import itemgetter
from collections import OrderedDict
import sys
import csv
import collections
import itertools

# Global Parameters:
# dict(counts) of all the subsets
itemSubsets = {}
# dict(counts) of frequent subsets(higher than min support)
freqItemSubsets = {}
# the association rules (Left-hand side is key, right-hand side is value)
associationRules = {}

#Calculate the 1-word subsets whose support is higher than threshold
def get1WordSubsets(rawData, minSup):
    #record all of the items (form all possible 1-word subsets)
    rowCount = 0
    itemSubsets_1 = {}
    for row in rawData:
    	row = set(row)
        #print row
        rowCount += 1
        for item in row:
            if item != 'NA' and item != 'N/A':
                items = [item]
                if item:
                    tup = tuple(items)
                    if tup in itemSubsets_1:
                        itemSubsets_1[tup] += 1
                    else:
                        itemSubsets_1[tup] = 1
    #print itemSubsets_1
    itemSubsets[1] = itemSubsets_1
    #Choose subsets whose support is higher than threshold
    freqItemSubsets_1 = {}
    for item, count in itemSubsets_1.iteritems():
        if count >= minSup * rowCount:
            freqItemSubsets_1[item] = count
    freqItemSubsets[1] = freqItemSubsets_1

#Fullfill itemSubsets & freqItemSubsets
def generateAllFreqSubsets(rawData, minSup):
    i_Large_Subsets = []
    for each in freqItemSubsets[1]:
        i_Large_Subsets.append(each)
    i = 2
    while i_Large_Subsets:
    	i_Candidate_Subsets = generateAllSubsets(i_Large_Subsets)
        i_itemSubsets = {}
        for row in rawData:
            row = set(row)
            count_i = countCandidate(row, i_Candidate_Subsets)
            for candidate in count_i:
                get_support(row, candidate, i_itemSubsets)

        itemSubsets[i] = i_itemSubsets
        i_freqItemSubsets = {}
        new_Large_Subsets = []
        for item, support in i_itemSubsets.iteritems():
            if support >= float(minSup) * len(rawData):
                i_freqItemSubsets[item] = support
                new_Large_Subsets.append(item)
        freqItemSubsets[i] = i_freqItemSubsets
        i_Large_Subsets = new_Large_Subsets
        
        i = i+1




#Generate all possible (i+1)-words subsets with i-words subsets
def generateAllSubsets(last_i_Large_Subsets):
    
    new_Candidate_Subset = [] 
    length = 0

    #Create all combinations
    for set1, set2 in itertools.combinations(last_i_Large_Subsets, 2):
    	#print set1
    	#print set2
        length = len(set1)
        if set1[:-1] == set2[:-1]:
            newItem = [set1[-1], set2[-1]]
            newSet = set1[:-1] + tuple(newItem)
            new_Candidate_Subset.append(newSet)
    
    #print new_Candidate_Subset
    # the prune step
    for itemset in new_Candidate_Subset:
        for subset in itertools.combinations(itemset, length):
            if not subset in last_i_Large_Subsets:
                #print subset
                new_Candidate_Subset.remove(itemset)
                break
    #print new_Candidate_Subset
    return new_Candidate_Subset

#Get items with in this row
def countCandidate(row, i_Candidate_Subsets):
    count_i = list(i_Candidate_Subsets)
    for subset in count_i:
        for item in subset:
            if not item in row:
                count_i.remove(subset)
                break
    return count_i

#Add support according to each row
def get_support(row, candidate, i_itemSubsets):
    if all(item in row for item in candidate):
        if candidate in i_itemSubsets:
            i_itemSubsets[candidate] += 1
        else:
            i_itemSubsets[candidate] = 1


def find_association(rawData, minConf):
    for right_Hand_Side in freqItemSubsets[1].keys():
        length = 0
        for value in freqItemSubsets.values():
            for left_Hand_Side, left_Hand_Side_Support in value.iteritems():
                length = len(left_Hand_Side)
                if all(i not in left_Hand_Side for i in right_Hand_Side):
                    for row in rawData:
                        if all(left_item in row for left_item in left_Hand_Side) and all(result_item in row for result_item in right_Hand_Side):
                            rule = '['
                            for left_item in left_Hand_Side:
                                rule += left_item + ','
                            rule = rule[:-1] + ']'
                            for result_item in right_Hand_Side:
                                rule += ' --> [' + result_item + ']'
                            if rule in associationRules:
                                associationRules[rule][0] += 1
                            else:
                                left1 = []
                                left1.append(1)
                                left1.append(left_Hand_Side_Support)
                                associationRules[rule] = left1

def printItout(minSup, minConf, numOfRows):
    with open('output.txt', 'wt') as output:
    	output.write("Itemsets whose support is larger than %f" % minSup + ':' +'\n')
    	freq_Item_Subsets =  [(y, freqItemSubsets[x][y]) for x in freqItemSubsets.keys() for y in freqItemSubsets[x].keys()]
        sorted_freq_Item_Subsets = sorted(freq_Item_Subsets, key=itemgetter(1), reverse=True)
        for row in sorted_freq_Item_Subsets:
            output.write("[{0}], {1:.1f}%".format(",".join(list(row[0])), float(row[1])/float(numOfRows) * 100) + '\n')
        output.write('\n'+'\n'+"Itemsets whose confidence is larger than %f" % minConf + ':' +'\n')
        sorted_rules = OrderedDict(sorted(associationRules.items(), key=lambda (k, (v1, v2)):[float(v1)/float(v2), v2], reverse=True))
        for row in sorted_rules:
            #print row
            confidence = float(sorted_rules[row][0])/float(sorted_rules[row][1])
            if confidence >= float(minConf):
                output.write("{0} (Conf: {1:.1f}%, Supp: {2:.1f}%)".format(row ,confidence*100, float(sorted_rules[row][1])/float(numOfRows)*100) + '\n')  

# the main function
def main():
    #judge input
    if len(sys.argv) == 4:
        datasetName = sys.argv[1]
        minSup = sys.argv[2]
        minConf = sys.argv[3]
        minSup = float(minSup)
        minConf = float(minConf)
    else:
        print 'How to run it: ' + "\n" + 'python hw3.py <input_data> <min_sup> <min_conf>'
        return

    if minSup>1 or minSup<0:
        print '<min_sup> shoule be a value between 0 and 1'
    if minConf>1 or minConf<0:
        print '<minConf> shoule be a value between 0 and 1'
    # Start to work with dataset
    with open(datasetName,'rU') as dataFile:
            reader = csv.reader(dataFile)
            rawData = list(reader)
            numOfRows = len(rawData)
            get1WordSubsets(rawData, minSup)
            generateAllFreqSubsets(rawData, minSup)
            #print itemSubsets[5]
            #print freqItemSubsets[4]
            find_association(rawData, minConf)
            #for each in associationRules:
            # 	print each
            printItout(minSup, minConf, numOfRows)
            #print "haha"
       

if __name__ == "__main__":
    #Call main function to run it
    main()