AssociationRuleMining
======

Authors
-------
    Li Niu (ln2334) and Yogesh Garg (yg2482)
    Project 3 Group 37

Files
-----
    Association_Finder.py
    INTEGRATED-DATASET
    output.txt
    xxxx
    README.md
    example-run.txt

A detailed description
----------
    a. We are using <311 Service Requests from 2010 to Present> to generate INTEGRATED-DATASET.csv.
    b. Yogesh’s work 
    c. Yogesh’s work 

A clear description of how to run your program 
-------
    Sample Command line: python association_rule.py <input_data> <min_sup> <min_conf>
    e.g. python Association_Finder.py INTEGRATED-DATASET.csv 0.3 0.8

A clear description of the internal design of your project
-----------
    1. We just read all from cvs file and store it in memory
    2. Then we iterate each row and generate the Set of large 1-itemset and filter it to get Set of candidate 1-itemset
    3. Use Algorithm Apriori  to find all existed Set of large k-itemset & Set of candidate k-itemset (Here is the pseudo code for it, figure-1 in the paper)
```
	1)  L1 = {large 1-itemsets};
	2)  for ( k = 2; Lk-1 # 0; k++ ) do begin
	3)    ck = apriori-gen(Lk-1); // New candidates
	4)    for all transactions t E D do begin
	5)        Ct = Subset(Ck, t); // Candidatea Contained in t
	6)        forall candidates c E Ct do
	7)            c.count++;
	8)    end
	9)    Lk = {C E ck | C.count >= minsup}
	10) end
	11) Answer = Uk Lk;
```
    4. We try to generate all possible association based on all Sets of candidate k-itemsets and keep those whose confidence is higher than threshold.
    5. Finally, we write all of them to output.txt.



The command line specification of an interesting sample run
-----------------------
    xxx

Additional Information
----------------------
    xxx
