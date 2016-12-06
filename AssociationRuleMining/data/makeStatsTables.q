
sd: 2010.01.01;
ed: 2016.12.31;

tBoroughByDate: select count i by `year$date, `mm$date, `$Borough from tCalls where date within (sd, ed);
save `:/tmp/tBoroughByDate.csv;
show count tBoroughByDate;

tAgencyByDate: select count i by `year$date, `mm$date, `$Agency_Name from tCalls where date within (sd, ed);
save `:/tmp/tAgencyByDate.csv;
show count tAgencyByDate;

tAgencyByDate: select count i by `year$date, `mm$date, `$Agency_Name from tCalls where date within (sd, ed);
save `:/tmp/tAgencyByDate.csv;
show count tAgencyByDate;

tComplaintByDate: select count i by `year$date, `mm$date, `$Complaint_Type from tCalls where date within (sd, ed);
save `:/tmp/tComplaintByDate.csv;
show count tComplaintByDate;

tZipByDate: select count i by `year$date, `mm$date, `$Incident_Zip from tCalls where date within (sd, ed);
save `:/tmp/tZipByDate.csv;
show count tZipByDate;

// .yo.aggf1: {[d] 0!select count(i) by date, `$Agency_Name, `$Complaint_Type, `$Descriptor, `$Location_Type, `$Incident_Zip, `$Borough from tCalls where date=d};
// .yo.aggf2: {[t] 0!select count(i) by `month$date, Agency_Name, Complaint_Type, Descriptor, Location_Type, Incident_Zip, Borough from t};

// aggdata : .yo.aggf2 raze .yo.aggf1 each 100#date;
// aggdata2: .yo.di each string aggdata;
// save `:/tmp/aggdata2.csv


