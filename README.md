# DataAutomation
Automation to consolidate data from csv file  ( )
  1. To excel (X)
  2. To graph ( )
able to calculate spec w/ w/t tempCo          ( )
retrieve data from raw data                   ( )
  1. Naming   ( )
  2. Unit SN  (X)
  3. PT No.   ( )
  4. Model Num(X)
  5. Nominal Val ( )
      a. Voltage    ( )
      b. Current    ( )
      c. Resistance ( )
      d. Power      ( )
  6. Naming using filename (>) - pending merge and user input 

ToDo: 
1. Remove get serial number and model number, get those info from CheckModel and CheckSN (from initDut)
2. Use df.merge(df2, on="Name"), sort keep it off
3. Make dataFrame for each test, only keep programming accuracy result for one, where graph is going to be gen from there (programming)
4. Only takes raw data, then calculate specs 
5. Tempco
6. Add option to collect only data, or plot graph
7. 
