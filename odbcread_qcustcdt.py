#!/QOpenSys/pkgs/bin/python3
#-------------------------------------------------------
# Module: odbcread_qcustcdt.py
# Desc: This sample reads table QIWS.QCUSTCDT and 
#       returns the data as JSON using ODBC and 
#       the IBM i Access ODBC Driver.
#
# Update Info:
# x/xx/xx - xxxxx
#------------------------------------------------
# Imports
#------------------------------------------------
import pyodbc
import sys
import time
import traceback
import json
from dbapp import DbApp

#------------------------------------------------
# Script initialization
#------------------------------------------------
#
#------------------------------------------------
# ODBC connection strings. 
#------------------------------------------------
# Run as specific user on selected system with soft coded connection string
#odbcconnstring= "Driver={IBM i Access ODBC Driver};System=1.1.1.1;Uid=USER01;Pwd=PASS01;CommitMode=0;EXTCOLINFO=1;"
#
# Set connection string. Normally this might be stored in a config file. 
# Run natively on IBM i as current user with *LOCAL DSN created by IBM i Access ODBC install
# Use this setting only if you NEVER want any committment control
# No committment control - *NONE isolation level
#odbcconnstring="DSN=*LOCAL;CommitMode=0;EXTCOLINFO=1;" 
#
# Use this setting by default and bypass committment control by using "with NC" in your SQL or using nocommit on execute()
# Enable committment control - *CS autocommit enabled.
odbcconnstring="DSN=*LOCAL;CommitMode=1;EXTCOLINFO=1;" 

# Instantiate DbApp application database layer and open connection
print("Open connection")
db = DbApp(odbcconnstring)

# If not open, bail out
if (db.isopen()==False):
   raise Exception("Connection not opened. Process cancelled.")

# Query customers
cursor1=db.query_qcustcdt("")

# If cursor returned, get all rows
if cursor1 != None:
   rows = cursor1.fetchall()
else:
   raise Exception(f"Query issue: {db.getlasterror()}")    

# Output records as JSON

# Get field metadata names from cursor
column_names = [desc[0] for desc in cursor1.description]

# Iterate and output data rows to array 
reccount=0
json_data=[]
for row in rows:
   # Return all fields as strings
   json_data.append(dict(zip(column_names,row)))       
   reccount += 1
   
print("{\"records\":" + f"{json.dumps(json_data,default=str)}" + "}")

print("Close connection")
db.close_connection()
