QProber
======

Authors
-------
Li Niu (ln2334) and Yogesh Garg (yg2482)
Project 2 Group 37

Files and Classes
-----------------

    .
    |-- APIKEY.txt                          # Contains all the APIKEY for our project
    |-- BingApi.py                          # Contains all the functions relevant to querying bing 
    |-- cache.BingApi.json                  # A cache is created so that we dont query too often
    |-- cache.lynx                          # This is a cache for lynx queries
    |   |-- http_es_fifa_com_live_score     #  | individual files
    |   |-- http_finance_yahoo_com_news     #  | individual files
    |   |-- http_fr_fifa_com_womens_foo     #  | individual files
    |   |-- http_www_health_com_health_     #  | individual files
    |   `-- .keys2file                      # url -> filename mapping
    |-- data                                # query files are kept here
    |   |-- computers.txt                   #
    |   |-- download.sh                     # they can be downloaded again using this file
    |   |-- health.txt                      #
    |   |-- root.txt                        #
    |   `-- sports.txt                      #
    |-- getWordsLynx.py                     #   a helper class for querying using lynx (cached in cache.lynx)
    |-- main.py                             #   *** this script is used to run our project ***
    |-- QProber.py                          #   most logic specific to QProber resides here e.g querying based on ts and tc, content summary generation
    |-- README.md                           #   You are reading this
    |-- Result.py                           #   methods for parsing Bing result
    |-- Topic.py                            #   we create a tree of topics, they reside here
    |-- util                                #
    |   |-- printAllLetters_char.txt        #   |
    |   |-- printAllLetters_int.txt         #   | we checked what Character.isLetter meant in java
    |   |-- printAllLetters.java            #   | currently we just use regex [A-Za-z]+ in python
    |   `-- printAllLetters.zip             #   |
    `-- Util.py                             #   this file is used for defining file and directory type caches, cool code inside!!!

How to Run
----------

    yg2482@delhi:~/code/Binger/QProber$ ./main.py 
    usage:
            ./main.py <API> <t_es> <t_ec> <host>
    yg2482@delhi:~/code/Binger/QProber$ ./main.py wRccq1TMy476bqFdC1GrKeHeJ33Fm+hmzSwYWgmtSrM= 0.6 1 fifa.com
    ...

Description
-----------
First of all, we create a class called "Topic" and build a category tree with whis class. In other word, each Topic object is a node in the tree and the root node could be used to represent the whole tree. For each node, there are many attributes, including name, subtopics, queries, parent,sampleCD. In the beginning we call root.load() to initialize these attributes according to the txt files (Root.txt, Health.txt, Sport.txt and Computers.txt). 
And then, I just search each query and record the both the number of results and top four urls for each node(topic). Then we could calculate coverage and specificity to define whether this node pass the threshold. If so, we will visit the subnodes of this node. If not, we will visit next node in the same level. (In other word, we judge and traversal with DFS)

We also add 4 samples each query while doing this probing, and propogate them upwards to parent nodes if any. This helps to later query for each node as described in the following paragraph.

To create content summaries, we download web page using lynx, ignore `References' section and ignore `\[\d+\]' patterns. Then we define a word as `[A-Za-z]+' pattern and find all such occurences. We count the number of occurences of each word.lower() for a document. We then sum these across documents for any given nodes. Python's Counter class is very helpful for this!

Bing Search Account Key
-----------------------
Added the api key in file called APIKEY.txt Our code can read the file automatically, but you have to provide it to the script if running through main.py

Additional Information
----------------------

We generate the content summaries for both queries and 1-grams, this means that items like "fan football" appear with `frequency in docs sampled' = 0 and `number of matches' > 0. For terms like acupuncture which are both queries and terms apearing in docs sampled, both the values are > 0. And for most terms, e.g. `the' which is not a query, `number of matches' = -1

Type sl on linux and take a break!!


