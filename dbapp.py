#-------------------------------------------------------
# Module: dbapp.py
# Desc: This module contains app specific queries
#       to support the application busines logic. 
#       The class inherits the DbIBMiOdbc database class
#       for accessing IBM i data via ODBC and the 
#       IBM i Access ODBC Driver
#       https://github.com/mkleehammer/pyodbc/
#-------------------------------------------------------
#
#-------------------------------------------------------
# Class: DbApp
# Desc: This class is a business layer that inherits 
# its IBM i database functonality from class DbIbmiOdbc
# which handles ODBC database access. It extends the
# functionality of DbIbmiOdbc for this specific app.
#-------------------------------------------------------
from dbibmiodbc import DbIbmiOdbc

class DbApp(DbIbmiOdbc):

    def insert_qcustcdt(self,cusnum,lstnam,init,street,city,state,zipcod,cdtlmt,chgcod,baldue,cdtdue,library='qiws',nocommit=False):
        #----------------------------------------------------------
        # Function: insert_qcustcdt
        # Desc: Insert new record into Customer Master
        # :param self: Pointer to object instance. 
        # :param field names: Each individual field name needed
        # :param library: IBMi library. Default=qiws
        # :param nocommit: Append "with NC" to end of SQL statment to avoid committment control
        #  True=append "with NC" to SQL for no commit. False=Perform commit. Default=False 
        # :return: True-Success, False-Error. Records affected also set to -2 on errors
        #----------------------------------------------------------
        try:
           # Create the SQL statement 
           sql = f"insert into {library}.qcustcdt (cusnum,lstnam,init,street,city,state,zipcod,cdtlmt,chgcod,baldue,cdtdue) VALUES({cusnum},'{lstnam}','{init}','{street}','{city}','{state}',{zipcod},{cdtlmt},{chgcod},{baldue},{cdtdue})"

           # Insert the record
           # Note: self parm not needed for execute when internal class function called
           rtnexecute=self.execute(sql,nocommit)
        
           # Return result value
           return rtnexecute
        
        except Exception as e:
            # Set error message
            self._lasterror=str(e)           
            print(e)

            return False

    def update_qcustcdt(self,cusnum,lstnam,init,street,city,state,zipcod,cdtlmt,chgcod,baldue,cdtdue,library='qiws',nocommit=False):
        #----------------------------------------------------------
        # Function: update_qcusctdt
        # Desc: Update existing record into Customer Master 
        # :param self: Pointer to object instance. 
        # :param field names: Each individual field name needed
        # :param library: IBMi library. Default=qiws
        # :param nocommit: Append "with NC" to end of SQL statment to avoid committment control
        #  True=append "with NC" to SQL for no commit. False=Perform commit. Default=False 
        # :return: True-Success, False-Error. Records affected also set to -2 on errors
        #----------------------------------------------------------
        try:
           # Create the SQL statement 
           sql = f"update {library}.qcustcdt set cusnum={cusnum},lstnam='{lstnam}',init='{init}',street='{street}',city='{city}',state='{state}',zipcod={zipcod},cdtlmt={cdtlmt},chgcod={chgcod},baldue={baldue},cdtdue={cdtdue} where cusnum={cusnum}"

           # Update the record. 
           # Note: self parm not needed for execute when internal class function called
           rtnexecute=self.execute(sql,nocommit)

           # Return result value
           return rtnexecute

        except Exception as e:
            # Set error message
            self._lasterror=str(e)           
            print(e)

            return False

    def delete_qcustcdt(self,cusnum,library='qiws',nocommit=False):
        #----------------------------------------------------------
        # Function: delete_qcustcdt
        # Desc: Delete record from Customer Master 
        # :param self: Pointer to object instance. 
        # :param cusnum - Customer to delete
        # :param library: IBMi library. Default=qiws
        # :param nocommit: Append "with NC" to end of SQL statment to avoid committment control
        #  True=append "with NC" to SQL for no commit. False=Perform commit. Default=False 
        # :return: True-Success, False-Error. Records affected also set to -2 on errors
        #----------------------------------------------------------
        try:
           # Create the SQL statement 
           sql = f"delete from {library}.qcustcdt where cusnum={cusnum}"
        
           # Delete the record
           # Note: self parm not needed for execute when internal class function called
           rtnexecute=self.execute(sql,nocommit)
        
           # Return result value
           return rtnexecute
        
        except Exception as e:
            # Set error message
            self._lasterror=str(e)           
            print(e)

            return False

    def getexists_qcustcdt(self,cusnum,library='qiws'):
        #----------------------------------------------------------
        # Function: getexists_qcustcdt
        # Desc: See if Customer Master record exists and return 
        # number of matching records.
        # :param self: Pointer to object instance. 
        # :param cusnum - Customer to check for
        # :param library: IBMi library. Default=qiws
        # :return: Result value from query
        #----------------------------------------------------------
        try:
           # Reset errors and rows affected
           self._lasterror=""
           self._lastsql=""
           self._rowsaffected=0 # Reset rows affected

           # Execute the query to get data
           cursor=self.execute_query(f"select count(*) as reccount from {library}.qcustcdt where cusnum={cusnum}")
           # Return result record count
           reccount =  cursor.fetchone()[0]

           # Return record count value from query
           return reccount
        
        except Exception as e:
            # Set error message
            self._lasterror=str(e)           
            print(e)

            # return -2 on error 
            return -2 

    def query_qcustcdt(self,wherestmt,library='qiws'):
        #----------------------------------------------------------
        # Function: query_qcustcdt
        # Desc: Query Customer Master table records with select where statement
        # :param self: Pointer to object instance. 
        # :param wherestmt - query where statement if desired
        # :param library: IBMi library. Default=qiws
        # :return: Resulting cursor or None on error
        #----------------------------------------------------------
        try:
         
           # Reset errors and rows affected
           self._lasterror=""
           self._lastsql=""
           self._rowsaffected=0 # Reset rows affected

           # Set main SQL     
           sql = f"select * from {library}.qcustcdt"

           # Add WHERE statement if criteria passed
           if wherestmt!="":
              sql = sql + " WHERE " + wherestmt

           # Save last SQL statement
           self._lastsql=sql

           # Execute the query to get data
           cursor=self.execute_query(sql)

           # Return results cursor
           return cursor
        
        except Exception as e:
            # Set error message
            self._lasterror=str(e)           
            print(e)
            
            # Return for no records
            return None
