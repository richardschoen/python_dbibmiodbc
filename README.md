# Python IBM i ODBC Database Class and Application Subclass
This repository contains a sample Python IBM i ODBC Database Class and Application Subclass for Structured Business App Logic.

```dbibmiodbc.py``` - This module contains a class named: DbIbmOdbc. This class is a wrapper for base ODBC database functionality without any other specific business logic. 
  
```dbapp.py``` - This module contains a class named: DbApp. This class inherits the DbIbmOdbc class and  should be used to create your own business specific application queries and business logic. 

```odbccrud_qcustcdt.py``` - This is a sample command line CLI script to exercise the DbIbmiOdbc and sample DbApp classes. The script will inert, update and delete a sample record from the QIWS.QCUSTCDT table and output the command results to the console.  

```odbcread_qcustcdt.py ``` - This is a sample command line CLI script  exercise the DbIbmiOdbc and sample DbApp classes. The script will read all records from the QIWS.QCUSTCDT table and output the data to the command line as JSON.  
