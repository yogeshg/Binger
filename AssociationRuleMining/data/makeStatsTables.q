\l hdb1/ 

sd: 2016.01.01;
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
.yo.unfold: {raze{(x`x)#enlist (x _ `x)}each 0!x};
// tAgencyComplaint: .yo.wash .yo.getMonthlyTableInCurrDates[`Agency_Name`Complaint_Type];
// save `:/tmp/tAgencyComplaint.csv;
// show count tAgencyComplaint;
//      29311
// tAgencyLocation: .yo.wash .yo.getMonthlyTableInCurrDates[`Agency_Name`Location_Type];
// save `:/tmp/tAgencyLocation.csv;
// show count tAgencyLocation;
//      18242
// tAgencyBorough: .yo.wash .yo.getMonthlyTableInCurrDates[`Agency_Name`Borough];
// save `:/tmp/tAgencyBorough.csv;
// show count tAgencyBorough;
//      17814
// tBoroughLocation: .yo.wash .yo.getMonthlyTableInCurrDates[`Borough`Location_Type];
// save `:/tmp/tBoroughLocation.csv;
// show count tBoroughLocation;
//      19264
// tBoroughZip: .yo.wash .yo.getMonthlyTableInCurrDates[`Borough`Incident_Zip];
// save `:/tmp/tBoroughZip.csv;
// show count tBoroughZip;
//      21299
// show .Q.gc[];
//      67108864

/ tABLf: .yo.wash .yo.getMonthlyTableInCurrDates[`Agency_Name`Borough`Location_Type];
/ save `:/tmp/tABLf.csv;
/ show count tABLf;
/ //        37733
/ tABL: .yo.wash .yo.unfold .yo.getMonthlyTableInCurrDates[`Agency_Name`Borough`Location_Type];
/ save `:/tmp/tABL.csv;
/ show count tABL;
/ //        37733

/ tABLCf: .yo.wash .yo.getMonthlyTableInCurrDates[`Agency_Name`Borough`Location_Type`Complaint_Type];
/ save `:/tmp/tABLCf.csv;
/ show count tABLCf;
/ //        81627
/ tABLC: .yo.wash .yo.unfold .yo.getMonthlyTableInCurrDates[`Agency_Name`Borough`Location_Type`Complaint_Type];
/ save `:/tmp/tABLC.csv;
/ show count tABLC;
/ //        81627

/ tABLCZf: .yo.wash .yo.getMonthlyTableInCurrDates[`Agency_Name`Borough`Location_Type`Complaint_Type`Incident_Zip];
/ save `:/tmp/tABLCZf.csv;
/ show count tABLCZf;
/ //        691568
/ tABLCZ: .yo.wash .yo.unfold .yo.getMonthlyTableInCurrDates[`Agency_Name`Borough`Location_Type`Complaint_Type`Incident_Zip];
/ save `:/tmp/tABLCZ.csv;
/ show count tABLCZ;
/ //        691568


tFinal:.yo.wash select Agency, Agency_Name, Borough, Location_Type, Street_Name, Complaint_Type, Descriptor, Incident_Zip from tCalls where date within (2016.01.01; 2016.12.31);
save `:/tmp/tFinal.csv;
show count tFinal;

show .Q.gc[];
//        603979776

\\