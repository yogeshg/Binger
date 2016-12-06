\l hdb1/ 

sd: 2010.01.01;
ed: 2016.12.31;

.qist.c:{(parse"select from t where ",x). 2 0 0};
.qist.b:{(parse"select by ",x," from t")3};
.qist.a:{(parse"select ",x," from t")4};

.yo.di: .Q.an!lower .Q.an;
.yo.bySymbols: {x!{($;enlist`;x)} each x};
.yo.byCastedColumn:{[x;y] x!{[x;y]($;enlist[x];y)}[;y] each x};

colnames:`Agency_Name`Complaint_Type;
// `Descriptor`Location_Type`Incident_Zip`Borough;

.yo.getMonthlyTable : {[colnames;sd;ed]
    AA:.qist.a "count i";
    CC:enlist(within;`date;(,;sd;ed));                            // .Q.s1 .qist.c "date within (sd,ed)"
    B1:{x!x}[enlist`date], .yo.bySymbols[colnames];
    B2:.yo.byCastedColumn[`year`mm;`date], {x!x}colnames;   // by month, symbols: 

    t1:?[`tCalls; CC; B1; AA];
    t2:?[t1; CC; B2; AA];
    :t2;
 }
.yo.getMonthlyTableInCurrDates:.yo.getMonthlyTable[;sd;ed];

.yo.wash: {.yo.di each string 0! x};

tAgencyComplaint: .yo.wash .yo.getMonthlyTableInCurrDates[`Agency_Name`Complaint_Type];
save `:/tmp/tAgencyComplaint.csv;
show count tAgencyComplaint;

tAgencyLocation: .yo.wash .yo.getMonthlyTableInCurrDates[`Agency_Name`Location_Type];
save `:/tmp/tAgencyLocation.csv;
show count tAgencyLocation;

tAgencyBorough: .yo.wash .yo.getMonthlyTableInCurrDates[`Agency_Name`Borough];
save `:/tmp/tAgencyBorough.csv;
show count tAgencyBorough;

tBoroughLocation: .yo.wash .yo.getMonthlyTableInCurrDates[`Borough`Location_Type];
save `:/tmp/tBoroughLocation.csv;
show count tBoroughLocation;

tBoroughZip: .yo.wash .yo.getMonthlyTableInCurrDates[`Borough`Incident_Zip];
save `:/tmp/tBoroughZip.csv;
show count tBoroughZip;

show .Q.gc[];
\\