# Python IBM i ODBC Database Access Class and Application Subclass
This repository contains a sample Python IBM i ODBC Database Class and Application Subclass for Structured Business App Logic.   

There are also a couple of scripts to actually exercise the ODBC driver wrapper class and the DbApp class. The scripts can be called from a command line in QShell or PASE or run on Windows, Linux or MacOS if you have the IBM i Access ODBC driver loaded. 

The scripts utilze the Python pyodbc ODBC wrapper and the IBM i Access ODBC Driver for connectivity.   

## Sample Python Script Project Files
The database code classes should work on IBM i, Windows, Linux or MacOS as long as the IBM i Access ODBC Driver is configured and working and Python 3 and pyodbc are installed. 

```dbibmiodbc.py``` - This module contains a class named: DbIbmOdbc. This class is a wrapper for base ODBC database functionality without any other specific business logic. The wrapper uses pyodbc and the IBM i Access ODBC Driver for connectivity. 
  
```dbapp.py``` - This module contains a class named: DbApp. This class inherits the DbIbmOdbc class and  should be used to create your own business specific application queries and business logic. 

```odbccrud_qcustcdt.py``` - This is a sample command line CLI script to exercise the DbIbmiOdbc and sample DbApp classes. The script will inert, update and delete a sample record from the QIWS.QCUSTCDT table and output the command results to the console.   

The ODBC connection string in the script is configured for a DSN of *LOCAL so the script can be run right from the IBM i system as a QShell or PASE commandl line call. It will use the current logged in user's credentials.
 
Ex call: ```python3 odbccrud_qcustcdt.py```

```odbcread_qcustcdt.py ``` - This is a sample command line CLI script  exercise the DbIbmiOdbc and sample DbApp classes. The script will read all records from the QIWS.QCUSTCDT table and output the data to the command line as JSON.    

The ODBC connection string in the script is configured for a DSN of *LOCAL so the script can be run right from the IBM i system as a QShell or PASE commandl line call. It will use the current logged in user's credentials.   

 Ex call: ```python3 odbccrud_qcustcdt.py```

 ## Using the Database Classes in Your Own Python Projects
The only files needed to use the database classes in your own projects are: ```dbibmiodbc.py``` and ```dbapp.py```.

The classes should work fine with command line apps, Flask apps, FastAPI apps or other apps where database access to an IBM i is needed.    

I'm not sure about using this class with the Django web framework, but if Django can utilize custom database call frameworks then it should work. I will test with Django at some point but that's not the main framework I use for Python web development. 


