#!/QOpenSys/pkgs/bin/python3
#-------------------------------------------------------
# Module: odbccrud_qcustcdt.py
# Desc: This sample deletes, inserts and updates a sample
#       record in table QIWS.QCUSTCDT using ODBC and 
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

# Delete all records with test key record - Commit will not happen because nocommit parm=True. 
rtnexec=db.delete_qcustcdt(121212,"QIWS",True)
print(f"Delete:{rtnexec} Error:{db.getlasterror()}")
print(f"LastSQL:{db.getlastsql()}")

if (rtnexec):
   print(f"Affected:{db.getlastrowsaffected()}")
else:
   print(f"Affected:{db.getlastrowsaffected()}")   
   print(f"Error:{db.getlasterror()}")   

# Insert a record - Commit will not happen because nocommit parm=True. 
rtnexec=db.insert_qcustcdt(121212,"Jameson","JA","12 Main","Mpls","MN",55001,1111,2,3.33,4.44,"QIWS",True)
print(f"Insert:{rtnexec} Error:{db.getlasterror()}")
print(f"LastSQL:{db.getlastsql()}")

if (rtnexec):
   print(f"Affected:{db.getlastrowsaffected()}")
else:
   print(f"Affected:{db.getlastrowsaffected()}")   
   print(f"Error:{db.getlasterror()}")   

# Check if records exists 
rtnexec=db.getexists_qcustcdt(121212,"QIWS")
print(f"getexists_qcustcdt record check. {rtnexec} records found. Error:{db.getlasterror()}")
   
# Update a record - Commit will not happen because nocommit parm=True. 
rtnexec=db.update_qcustcdt(121212,"Jameson","JA","13 Main","Mpls","MN",55003,3333,2,3.33,4.44,"QIWS",True)
print(f"Update:{rtnexec} Error:{db.getlasterror()}")
print(f"LastSQL:{db.getlastsql()}")
   
if (rtnexec):
   print(f"Affected:{db.getlastrowsaffected()}")
else:
   print(f"Affected:{db.getlastrowsaffected()}")   
   print(f"Error:{db.getlasterror()}")   

print("Close connection")
db.close_connection()
