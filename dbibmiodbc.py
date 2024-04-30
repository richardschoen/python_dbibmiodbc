#-------------------------------------------------------
# Module: dbibmiodbc.py
# Desc: This module contains our IBM i database parent 
#       class for accessing IBM i data via ODBC and the 
#       IBM i Access ODBC Driver
#       https://github.com/mkleehammer/pyodbc/
#
# Update Info:
# 4/29/2024 - Initial version 
#
# Links:
#
# Committment control
# https://www.youtube.com/watch?v=-LPjcufeibE
#
# IBM i Access ODBC COmmittment Control
# https://www.ibm.com/support/pages/ibm-i-access-odbc-commit-mode-data-source-setting-isolation-level-and-autocommit
# -7008 or SQL7008 may occur when table not journaled and commit control enabled. Need to enable table journaling or
# disable committment control in connection string.
#
# Bypass committment control "with NONE" or "with NC"
# https://www.ibm.com/docs/en/db2/11.5?topic=errors-sql7008n
# insert into <tableName> values ('a', 'b') with NC
# insert into <tableName> values ('a', 'b') with NONE
#-------------------------------------------------------
#
# Environment setup
# pip install --upgrade pyodbc
#
#-------------------------------------------------------
# Class: DbIbmiOdbc
# Desc: This class is a wrapper class around IBM i 
#       ODBC database functions
#-------------------------------------------------------
import pyodbc as db2
import uuid
import sqlparams

class DbIbmiOdbc():
 
    # Class variables
    _dbopen=False
    _dbconn=None
    _dbconnstring=""
    _lasterror=""
    _lastsql=""
    _rowsaffected=0

    def __init__(self,db_connstring=None):
        #-------------------------------------------------------
        # Function: __init__
        # Desc: Constructor
        # :param self: Object instance
        # :param db_file: File name or default to None if no file 
        #        needs to be opened yet
        # :return: Connection or None on error 
        #-------------------------------------------------------
        try:
           _dbopen=False
           _dbconn=None
           if db_connstring != None and db_connstring != "":
              self.create_connection(db_connstring)
           else:
              print("No ODBC connection string passed in. Need to create connection later.")
        except Exception as e:
            print(e)
        finally:
            return None #Can return None or omit any return
 
    def getnewguid(self):
        #----------------------------------------------------------
        # Function: getnewguid
        # Desc: Generate new GUID using the uuid1 function
        # :param self: Pointer to object instance. 
        # :return: Resulting guid or None
        #----------------------------------------------------------
        try:
           # generate the guid (uuid1)
           return uuid.uuid1()
        except Error as e:
            print(e)  
            return None
        
    def getlasterror(self):
        #-------------------------------------------------------
        # Function: getlasterror
        # Desc: Get last error from the class
        # :param self: Pointer to object instance. 
        # :return: internal -lasterror value
        #-------------------------------------------------------
        return self._lasterror

    def getlastrowsaffected(self):
        #-------------------------------------------------------
        # Function: getlastrowsaffected
        # Desc: Get last rows affected from SQL execute. This value
        # should contain number of records affected value or -2 on error.
        # :param self: Pointer to object instance. 
        # :return: internal rowsaffected value
        #-------------------------------------------------------
        return self._rowsaffected

    def getlastsql(self):
        #-------------------------------------------------------
        # Function: getlastsql
        # Desc: Get last sql executed from the class.
        # :param self: Pointer to object instance. 
        # :return: internal last sql value
        #-------------------------------------------------------
        return self._lastsql

    def isopen(self):
        #-------------------------------------------------------
        # Function: isopen
        # Desc: Check if database is open 
        # :param self: Pointer to object instance. 
        # :return: True-Db is open, False=Db is not open
        #-------------------------------------------------------
        #return DB open status
        return self._dbopen

    def getconn(self):
        #-------------------------------------------------------
        # Function: getconn
        # Desc: Get database connection object 
        # :param self: Pointer to object instance. 
        # :return: Connection value
        #-------------------------------------------------------
        #return conn object
        return self._dbconn
    
    def create_connection(self,db_connstring):
        #-------------------------------------------------------
        # Function: create_connection
        # Desc: Create a database connection to IBMi database via ODBC
        # :param self: Pointer to object instance. 
        # :param db_connstring: ODBC connection string for IBM i
        # :return: True-Connection open, False-No connection open 
        #-------------------------------------------------------

        #Create connection variable
        conn = None 

        #Let's try and open the database. Will auto-create if not found.
        try:
            conn = db2.connect(db_connstring)

            # Set open flag = true
            if conn != None:
               #Save open connection info internally in the class 
               self._dbopen=True 
               self._dbconn = conn
            return self._dbopen;
        except Exception as e:
            print(e)
            return False

    def close_connection(self):
        #-------------------------------------------------------
        # Function: close_connection
        # Desc: Close a database connection to a SQLite database 
        # :param self: Pointer to object instance. 
        # :return: True-Success, False-Error
        #-------------------------------------------------------

        # Let's attempt to close our database connection 
        try:
            self._dbconn.close()
            #Release object. Not sure if needed or automatic ?
            conn=None
            self._dbconn=None
            return True;
        except Exception as e:
            print(e)
            return False

    def execute(self,sql,nocommit=False,debug=False):
        #----------------------------------------------------------
        # Function: execute
        # Desc: Execute an SQL action query that does not return results
        # :param self: Pointer to object instance. 
        # :param sql: SQL action query
        # :param nocommit: Append "with NC" to end of SQL statment to avoid committment control
        #  True=append "with NC" to SQL for no commit. False=Perform commit. Default=False 
        # :return: True-Success, False-Error. Records affected also set to -2 on errors
        #----------------------------------------------------------
        try:
            
            # Reset errors and rows affected
            self._lasterror=""
            self._rowsaffected=0 # Reset rows affected
            self._lastsql=""
            
            # Get connection
            conn1 = self._dbconn

            # If no commit, add "with NC" to end of SQL
            if (nocommit): 
               # Check if "with nc" already ends the statement. 
               # If so, don't add "with nc"
               if (sql.lower().endswith("with nc")==False): 
                  sql=f"{sql} with NC"

            # Print SQL if debug enabled
            if (debug):               
               print(f"SQL:{sql}")   
            
            # Start transaction  - if enabled      
            # Note: pyodbc has no actual 
            # Begin transaction method
            # So this is here just to document
            # Must issue commit or rollback
            # when committment control enabled
            # Print debug info if debug enabled
            if (debug):               
               print("Transaction Begin") 

            # Save last SQL statement
            self._lastsql=sql
                
            #Execute the action query                
            results=conn1.execute(sql) 

            #Save rows affected
            # https://github.com/mkleehammer/pyodbc/issues/829
            self._rowsaffected=results.rowcount

            # Commit transaction. 
            # Actual commit appears to be 
            # ignored if CommitMode=0 on connection
            conn1.commit()
            
            # Print debug info if debug enabled
            if (debug):               
                print("Transaction Commit") 

            self._lasterror="SQL execute action appears to have completed."
            
            return True
        except Exception as e:
            # Set error message
            self._lasterror=str(e)
            print(e)  

            # Set rows affected to -2 to indicate errors
            self._rowsaffected=-2

            # Roll back any changes                        
            # Actual rollback appears to be 
            # ignored if CommitMode=0 on connection
            self._dbconn.rollback() 

            # Print debug info if debug enabled
            if (debug):               
               print("Transaction Rollback") 

            return False

    def executeiwthparms(self,sql,parms,nocommit=False,debug=False):
        #----------------------------------------------------------
        # Function: executewithparms
        # TODO: Need to test with parameter markers.
        # Desc: Execute an SQL action query that does not return results
        # :param self: Pointer to object instance. 
        # :param sql: SQL action query
        # :param nocommit: Append "with NC" to end of SQL statment to avoid committment control
        #  True=append "with NC" to SQL for no commit. False=Perform commit. Default=False 
        # :param parms: SQL parameters array
        # :return: True-Success, False-Error. Records affected also set to -2 on errors
        #----------------------------------------------------------
        try:
            
            # Reset errors and rows affected
            self._lasterror=""
            self._rowsaffected=0 # Reset rows affected
            self._lastsql=""
            
            # Get connection
            conn1 = self._dbconn

            # If no commit, add "with NC" to end of SQL
            if (nocommit): 
               # Check if "with nc" already ends the statement. 
               # If so, don't add "with nc"
               if (sql.lower().endswith("with nc")==False): 
                  sql=f"{sql} with NC"

            # Print SQL if debug enabled
            if (debug):               
               print(f"SQL:{sql}")   
            
            # Start transaction  - if enabled      
            # Note: pyodbc has no actual 
            # Begin transaction method
            # So this is here just to document
            # Must issue commit or rollback
            # when committment control enabled
            # Print debug info if debug enabled
            if (debug):               
               print("Transaction Begin") 

            # Save last SQL statement
            self._lastsql=sql
                
            #Execute the action query with parameters
            results=conn1.execute(sql,parms) 

            #Save rows affected
            # https://github.com/mkleehammer/pyodbc/issues/829
            self._rowsaffected=results.rowcount

            # Commit transaction. 
            # Actual commit appears to be 
            # ignored if CommitMode=0 on connection
            conn1.commit()
            
            # Print debug info if debug enabled
            if (debug):               
                print("Transaction Commit") 

            self._lasterror="SQL executewithparms action appears to have completed."
           
            return True
        except Exception as e:
            # Set error message
            self._lasterror=str(e)
            print(e)  

            # Set rows affected to -2 to indicate errors
            self._rowsaffected=-2

            # Roll back any changes                        
            # Actual rollback appears to be 
            # ignored if CommitMode=0 on connection
            self._dbconn.rollback() 

            # Print debug info if debug enabled
            if (debug):               
               print("Transaction Rollback") 

            return False

    def execute_query(self,sql):
        #----------------------------------------------------------
        # Function: execute_query
        # Desc: Execute an SQL query that does return results
        # :param self: Pointer to object instance. 
        # :param sql: SQL query expecting results
        # :return: Resulting cursor or None on error
        #----------------------------------------------------------
        try:

            # Reset errors and rows affected
            self._lasterror=""
            self._lastsql=""
            self._rowsaffected=0 # Reset rows affected
   
            # Save last SQL statement
            self._lastsql=sql

            # Run SQL query 
            cursor1 = self._dbconn.cursor()
            cursor1.execute(sql)

            # Return results cursor
            return cursor1

        except Exception as e:
            # Set error message
            self._lasterror=str(e)
            print(e)  
            return None
     
