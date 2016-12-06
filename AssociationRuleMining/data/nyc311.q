// this code is in q language
// please look at code.kx.com for syntax

.yo.write2hdb:{[d;tcsv]                                                         // function write2hdb( date d, table tcsv )
    t:.yo.c xcol (.yo.ct;enlist",")0: hsym tcsv;                                //          rename columns to .yo.c after reading csv file tcsv of column types .yo.ct
    t:update date:("D"$10#)each Created_Date,sym:`  from t;                     //          add a date column by parsing dates in Created_Date column
    t:t,get `tBuff;                                                             //          append tBuff, a buffer table that stores entries of minimum date of last chunk
    `tBuff set select from t where date=min[date];                              //          set tBuff to store minimum date, we do this because we write to hard disk one date at a time
    t:select from t where date>min[date];                                       //          only write to hardisk for dates greater than minimum date
    {[d;p;f;tn;t]                                                               //          lambda (date, partition, file, tablename, table)
        tn set select from t where date = p;                                    //                  // code snippet from
        .Q.dpft[d;p;f;tn];                                                      //                  // code snippet from
    }[d;;`sym;`tCalls;t] each exec distinct date from t;                        //          apply curried to (date, ,enumeration_file, table name, table data) apply for each date
 }                                                                              // end
.yo.c:get `:colnames3;                                                          // read column names
// where .yo.c in `Latitude`Longitude                                           //
.yo.ct:53#"*";                                                                  // all column types are strings
.yo.ct[50]:"J";                                                                 // 50, 51 column types are long integers
.yo.ct[51]:"J";                                                                 //
.yo.cwd:"/Users/yogeshgarg/Code/adb/Binger/AssociationRuleMining/data";         // working directory
.yo.db:hsym`$.yo.cwd,"/hdb1/";                                                  // create date partitioned database in this directory
                                                                                //
                                                                                //
`tBuff set ();                                                                  // initialise tBuff
                                                                                //
.yo.write2hdb[.yo.db;`taa];show .Q.gc[];                                        // run for different splits of csv files
.yo.write2hdb[.yo.db;`tab];show .Q.gc[];
.yo.write2hdb[.yo.db;`tac];show .Q.gc[];
.yo.write2hdb[.yo.db;`tad];show .Q.gc[];
.yo.write2hdb[.yo.db;`tae];show .Q.gc[];
.yo.write2hdb[.yo.db;`taf];show .Q.gc[];
.yo.write2hdb[.yo.db;`tag];show .Q.gc[];
.yo.write2hdb[.yo.db;`tah];show .Q.gc[];
.yo.write2hdb[.yo.db;`tai];show .Q.gc[];
.yo.write2hdb[.yo.db;`taj];show .Q.gc[];
.yo.write2hdb[.yo.db;`tak];show .Q.gc[];

.yo.write2hdb[.yo.db;`tal];show .Q.gc[];
.yo.write2hdb[.yo.db;`tam];show .Q.gc[];
.yo.write2hdb[.yo.db;`tan];show .Q.gc[];
.yo.write2hdb[.yo.db;`tao];show .Q.gc[];
.yo.write2hdb[.yo.db;`tap];show .Q.gc[];
.yo.write2hdb[.yo.db;`taq];show .Q.gc[];
.yo.write2hdb[.yo.db;`tar];show .Q.gc[];
.yo.write2hdb[.yo.db;`tas];show .Q.gc[];
.yo.write2hdb[.yo.db;`tat];show .Q.gc[];
.yo.write2hdb[.yo.db;`tau];show .Q.gc[];

