Binger
======

Authors
-------
Li Niu (ln2334) and Yogesh Garg (yg2482)
Project 1 Group 37

Files
-----
    BingApi.py
    Binger.py
    Reult.py
    QueryExpander.py
    main.py

How to Run
----------
Part1: First of all, run the program with command line python main.py . Then input your query word, and the expected precision@10.

    ./main.py apikey query precision10

    ./main.py `cat API*` 'Bing Chandler' 0.9

Part2: After that, 10 results will be displayed and the users need to input 0 or 1 to judge whether the result is relevant. (0 means irrelevant, 1 means relevant).

    > Result 1 is displayed
    <Enter Relevance on prompt>
    > Result 2 is displayed
    <Enter Relevance on prompt>
    .
    .
    .
    > Result 10 is displayed
    <Enter Relevance on prompt>

If the precision@10 is 0 or higher than the expected one, the program will be terminated. If not, the program will generate a new query according to the user feedback and present another 10 results.
    <Repeat Part 2>

Classes
-------
    BingApi -- Class for contacting Bing and related util functions
    Binger -- Class for the logic of this app
    Result -- Class for defining what Bing Results look like
    QueryExpander -- Class for generating the new query.
    main.py -- this is the file that is run by the user. It calls the various moving parts.

Description
-----------
For the QueryExtender, we grab all words from the titles, URLs and the description of the website. These words are stored in a list. Then, we calculate the idf for each single word and store the value in the same sequence as the words. After that, we generate a 2-D list to store the tf info for each word in each single documents. Then, we could also obtain the tf-idf matrix. Then, we could generate a ‘Final score’ using Rocchio Algorithm. Because the sequence of the words is as same as the sequence in score list, we could find the single best word according to the index of the max value in score list. (The expander can only add 1 word in each single iteration)

Bing Search Account Key
-----------------------
Added the api key in file called APIKEY.txt

Additional Information
----------------------

Type sl on linux and take a break!!

