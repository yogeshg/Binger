AssociationRuleMining
=====================

Authors
-------

This is the work of Group 37

 * Li Niu (ln2334)
 * Yogesh Garg (yg2482)

for the Project 3 of Advanced Database Systems, COMS 611, fall 2016.

Files
-----

    $ tree .
    .                             # 
    ├── Association_Finder.py     # This python file contains the code to
    │                             #   process the dataset and algorithm
    │                             #   described in one of the sections
    ├── README.md                 # 
    ├── Util.py                   # Utilities we no longer use (caching etc.)
    ├── data                      # Subfolder containing datasets
    │   ├── data_311.csv          # the actual dataset (not included)
    │   ├── download.sh           # script to download the actual dataset
    │   ├── nyc311.q              # q/kdb script to process csv chunks into hdb
    │   ├── makeStatsTables.q     # this script is used create a cut of the
    │   │                         #   data for our algorithm as discussed below
    │   ├── download_final.sh     # script to download a copy of final dataset
    │   ├── tFinal.csv            # the generated data, not included in the repo
    │   │                         #   but it can be downloaded using the above
    │   │                         #   script or following the steps described
    │   ├── tFinal_sample.csv     # sample of generated data
    ├── output.txt                # output file is created here
    ├── output_tFinal_10_75.txt   # output for 10pc support and 75pc confidence
    ├── output_tFinal_10_90.txt   # output for 10pc support and 90pc confidence
    └── output_tFinal_20_90.txt   # output for 20pc support and 90pc confidence

Dataset (a detailed description)
--------------------------------

* we are using [nycdata311](nycdata311) to generate `tFinal.csv`
* as described on the website, this dataset contains
  > All 311 Service Requests from 2010 to present. This information is automatically
  > updated daily.
* we check the size of data, it has 14 million rows
```
    $ wc -l data_311.csv
     14099926

    $ du -sh data_311.csv
    8.8G    data_311.csv
```
* to view the distribution of columns and select the relevant ones, we want to
  create a kdb database for this csv
* this would require a file to be read in memory in chunks and written to a
  file based database partitioned by date
* the free version of kdb can only process 4GB data in RAM, so we decide to cut
  the database in 10 parts
```
    $ split -l 1400000 data_311.csv
    $ wc -l t*
     1400000 taa
     1400000 tab
     1400000 tac
     1400000 tad
     1400000 tae
     1400000 taf
     1400000 tag
     1400000 tah
     1400000 tai
     1400000 taj
       99926 tak
```
* We still failed to fit each chunk into memory and we had to split the data
  into half the size which means 20 parts
```
    $ du -sh ta*
    459M    taa
    437M    tab
    451M    tac
    443M    tad
    437M    tae
    459M    taf
    457M    tag
    416M    tah
    406M    tai
    452M    taj
    458M    tak
    449M    tal
    457M    tam
    441M    tan
    457M    tao
    445M    tap
    449M    taq
    454M    tar
    438M    tas
    458M    tat
     65M    tau
```
* Using [nyc311.q](nyc311_q), we write these split csv files to kdb format database
* this allows us to write queries like following and run on the entire dataset
```
    q)t2: select count[i] by year:`year$date, borough from tCalls;
    q)exec borough!numrows by year:year from 0!t2
```
year| BRONX  |BROOKLYN |MANHATTAN |QUEENS |STATEN ISLAND |Unspecified
---:|-------:|--------:|---------:|------:|-------------:|----------:
2010| 88356  |169632   |120473    |162046 |37770         |334178
2011| 204332 |332209   |210145    |238468 |56911         |66228
2012| 258597 |408595   |258915    |294427 |59381         |39439
2013| 236392 |375026   |247907    |252290 |51057         |53422
2014| 114816 |174184   |119113    |119138 |21266         |19629
2015| 51250  |71428    |45711     |47714  |8384          |13960
2016| 34694  |57456    |42059     |43633  |8909          |8549
```
    // for about agency that constituite 90% of the data
    q)exec d1^(`$string year)!numrows by agency:agency from t3
```
agency                                            | 2010   |2011   |2012   |2013   |2014   |2015   |2016
--------------------------------------------------| ------:|------:|------:|------:|------:|------:|----:
BCC - Brooklyn South                              | 6540   |6646   |7965   |7876   |3904   |1487   |1754
DHS Advantage Programs                            | 14162  |13943  |2833   |99     |5      |3      |2200
Department for the Aging                          | 4656   |5891   |7882   |6721   |2366   |1075   |534
Department of Buildings                           | 53028  |49644  |64847  |55092  |23782  |6573   |7446
Department of Consumer Affairs                    | 10966  |12921  |17347  |13983  |5377   |1801   |1530
Department of Environmental Protection            | 8613   |92499  |6113   |1841   |1178   |2367   |14310
Department of Finance                             | 13757  |1828   |17009  |29004  |7060   |5286   |3446
Department of Health and Mental Hygiene           | 21887  |26897  |37062  |32064  |13843  |4165   |4880
Department of Housing Preservation and Development| 322044 |398137 |455989 |415038 |205966 |100416 |45525
Department of Parks and Recreation                | 47416  |57559  |89967  |57958  |20916  |3816   |6637
Department of Sanitation                          | 8813   |4492   |11271  |8965   |492    |1225   |1786
Department of Transportation                      | 150559 |149289 |202465 |192250 |74209  |34810  |20930
New York City Police Department                   | 172753 |178121 |246764 |262122 |149284 |46023  |61030
Refunds and Adjustments                           | 4314   |5017   |7666   |6964   |3450   |1077   |568
Senior Citizen Rent Increase Exemption Unit       | 4143   |8941   |12222  |5635   |2393   |853    |449
Taxi and Limousine Commission                     | 13757  |14148  |18265  |14191  |6222   |1853   |2200

* after looking at **many** cuts of data, we settle for the following view to create our integrated dataset:
```
    q) tFinal:.yo.wash select Agency, Agency_Name, Borough, Location_Type, Street_Name,
                Complaint_Type, Descriptor, Incident_Zip from tCalls
                where date within (2016.01.01; 2016.12.31);
    q) save `:/tmp/tFinal.csv;
    q) show count tFinal;
```

* we select the following columns and consider the **created_date for 2016**:
  - Agency
  - Agency_Name
  - Borough
  - Location_Type
  - Street_Name
  - Complaint_Type
  - Descriptor
  - Incident_Zip
* we chose this cut for analysis because
  - This contains most relevant columns, some of which are correlated and some
    un-correlated
  - We delete many columns that contain very sparse data like school name, which
    seems to be very specifically tailored to a specific type of call
  - We use one year's worth of data, to ensure we do not miss out any artefact
    that may arise due to season

* `data/tFinal.csv` contains 195300 records and ```data/tFinal_sample.csv```
  contains 1999 records
```
    $ wc -l tFinal*.csv
      195301 tFinal.csv
        2000 tFinal_sample.csv
```

The Algorithm
-------------
* We just read all from cvs file and store it in memory
* Then we iterate each row and generate the Set of large 1-itemset and filter
  it to get Set of candidate 1-itemset
* Use Algorithm Apriori  to find all existed Set of large k-itemset and Set of
  candidate k-itemset (Here is the pseudo code for it, figure-1 in the
  [paper](VLDB)
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
* We try to generate all possible association based on all Sets of candidate
  k-itemsets and keep those whose confidence is higher than threshold.
* Finally, we write all of them to output.txt.

How to Run
----------
```
    $ python Association_Finder.py
    usage: 
        python association_rule.py <input_data> <min_sup> <min_conf>

    $ python Association_Finder.py data/tFinal_sample.csv 0.2 0.9
    $ ./data/download_final.sh
    $ python Association_Finder.py data/tFinal.csv 0.2 0.9
    $ mv output.csv output_tFinal_20_90.csv
    $ python Association_Finder.py data/tFinal.csv 0.1 0.9
    $ mv output.csv output_tFinal_10_90.csv
    $ python Association_Finder.py data/tFinal.csv 0.1 0.75
    $ mv output.csv output_tFinal_10_75.csv
```

Results
-------
* we get all proper nouns with 20pc support, for example
  ```
  [NYPD,New York City Police Department], 31.2%
  [BROOKLYN], 29.4%
  [HPD], 23.3%
  ```
* We are able to find a few full forms in our dataset using this configuration
  ```
  [New York City Police Department] --> [NYPD] (Conf: 100.0%, Supp: 31.2%)
  [HPD] --> [Department of Housing Preservation and Development] (Conf: 100.0%, Supp: 23.3%)
  [Department of Housing Preservation and Development] --> [HPD] (Conf: 100.0%, Supp: 23.3%)
  [Department of Housing Preservation and Development] --> [RESIDENTIAL BUILDING] (Conf: 99.4%, Supp: 23.3%)
  ```
* We also come up with some very simple rules like
  ```
  [RESIDENTIAL BUILDING] --> [HPD] (Conf: 100.0%, Supp: 23.2%)
  ```
* By using 10 pc support, we get a few more interesting lines 
  ```
  +[Noise - Residential,Residential Building/House] --> [NYPD] (Conf: 100.0%, Supp: 10.2%)
  +[Loud Music/Party] --> [New York City Police Department] (Conf: 100.0%, Supp: 10.1%)
  +[Street/Sidewalk] --> [NYPD] (Conf: 94.4%, Supp: 18.7%)
  ```
* We incrementally decrease support and look at some interesting rules we received with 5pc support
  ```
  +[HEAT/HOT WATER] --> [Department of Housing Preservation and Development] (Conf: 100.0%, Supp: 8.0%)
  +[Department of Environmental Protection] --> [DEP] (Conf: 100.0%, Supp: 7.3%)
  +[Blocked Driveway] --> [NYPD] (Conf: 100.0%, Supp: 5.9%)
  +[Illegal Parking] --> [NYPD] (Conf: 100.0%, Supp: 5.7%)
  +[DEP] --> [Department of Environmental Protection] (Conf: 99.8%, Supp: 7.3%)
  ```
* with 2pc support,
  ```
  +[No Access,NYPD] --> [Blocked Driveway] (Conf: 100.0%, Supp: 4.3%)
  +[DOB] --> [Department of Buildings] (Conf: 100.0%, Supp: 3.8%)
  +[Street Light Out] --> [DOT] (Conf: 100.0%, Supp: 2.9%)
  ```
* with 1pc support,
  ```
  +[PESTS] --> [HPD] (Conf: 100.0%, Supp: 1.8%)
  +[Pothole] --> [DOT] (Conf: 100.0%, Supp: 1.7%)
  +[Traffic Signal Condition] --> [DOT] (Conf: 100.0%, Supp: 1.5%)
  +[Benefit Card Replacement] --> [HRA] (Conf: 100.0%, Supp: 1.2%)
  ```

Conclusions
-----------
* Some of the information that we were able to get is listed
  - We are able to quickly find full-forms for more popular departments first
  - By decreasing support, we also get many other full-forms also
  - We are able to learn that NYPD is called to deal with Loud Music, Parties or Residential Noise
  - Department of Housing Preservation and Development is associated with complains in Residential Buildings 
  - For heat and hot water related problems, you should call upon HPD.
  - For blocked driveway or illegal parking, you could call NYPD.
  - For street lights, you wanna go to DOT
  - If there is an issue related to Pothole or Traffic Signal Condition,
    we could go to DOT
  - For Benefit Card Replacement, go to HRA
* With decreasing support, we easily come up with rules that are valid
 but were earlier hidden because they were very few
* We also noticed that with decreasing confidence we dont necessarily
 come up with newer results

References
----------
* [assignment_description](http://www.cs.columbia.edu/~gravano/cs6111/proj3.html):
    Assignment description.
* [VLDB](http://www.cs.columbia.edu/~gravano/Qual/Papers/agrawal94.pdf):
    Rakesh Agrawal and Ramakrishnan Srikant: Fast Algorithms for Mining Association Rules in Large Databases, VLDB 1994.
* [nycdata311](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9):
    The source of original data.
* [nyc311_q](https://github.com/yogeshg/DI/tree/master/nyc311):
    The code used to generate kdb from csv is adapted from one of the author's
    previous projects.
