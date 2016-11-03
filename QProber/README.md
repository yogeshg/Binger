QProber
======

Authors
-------
Li Niu (ln2334) and Yogesh Garg (yg2482)
Project 2 Group 37

Files
-----
    BingApi.py
    QProber.py
    Reult.py
    Topic.py
    main.py
    APIKEY.txt
    README.md
    xxxxxx
    xxxxxx

How to Run
----------
xxxxxx
xxxxxx

Classes
-------
    BingApi -- Class for contacting Bing and related util functions
    QProber -- Class that implement QProber
    Result -- Class for defining what Bing Results look like
    xxxxxx
    xxxxxx
    xxxxxx
    main.py -- this is the file that is run by the user. It calls the various moving parts.

Description
-----------
First of all, we create a class called "Topic" and build a category tree with whis class. In other word, each Topic object is a node in the tree and the root node could be used to represent the whole tree. For each node, there are many attributes, including name, subtopics, queries, parent,sampleCD. In the beginning we call root.load() to initialize these attributes according to the txt files (Root.txt, Health.txt, Sport.txt and Computers.txt). 
And then, I just search each query and record the both the number of results and top four urls for each node(topic). Then we could calculate coverage and specificity to define whether this node pass the threshold. If so, we will visit the subnodes of this node. If not, we will visit next node in the same level. (In other word, we judge and traversal with DFS)
xxxxxx
xxxxxx
xxxxxx

Bing Search Account Key
-----------------------
Added the api key in file called APIKEY.txt (Our code will read the file automatically)

Additional Information
----------------------

Type sl on linux and take a break!!

