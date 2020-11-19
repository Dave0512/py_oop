import pyodbc

class Database:
    """
    Class to connect, and interact with several types of relational dbms
    like ms sql server, mySQL, PostgreSQL, SQLite
    """
    def __init__(self,driver, server, database,tr_conn):
        """
        Method recieves compulsory parameter 
        to create a connection to a database.

        MS SQL Server, for instance:
        "DRIVER={SQL Server Native Client 11.0};"
        "SERVER=192.168.16.124;"
        "DATABASE=Vorlauf_DB;"
        "Trusted_Connection=yes;
        """
        self._db_conn = pyodbc.connect(r"DRIVER={0};"
                                           "SERVER={1};"
                                           "DATABASE={2};"
                                           "Trusted_Connection={3};".format(driver, server, database,tr_conn))

    