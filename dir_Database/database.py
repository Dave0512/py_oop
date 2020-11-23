import pyodbc

class Database:
    """
    Class to connect, and interact with several types of relational dbms
    like ms sql server, mySQL, PostgreSQL, SQLite

    Documentation:
        Database Handler Class
        1) Open Database (Using "with" to easy handle db_connection)
        2) Set a cursor
        3) Commit data 
            "Each SQL command is in a transaction and the transaction 
             must be committed to write the transaction 
             to the SQL Server so that it can be read by other SQL commands.

             Under MS SQL Server Management Studio the default is to allow 
             auto-commit which means each SQL command immediately 
             works and you cannot rollback."
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

        self._cursor = self._db_conn.cursor()

    def __enter__(self):
        """
        Magic method to let the class use the with statement.
        """
        return self

    def __exit__(self,exc_type,exc_val,exc_tb):
        """
        Magic method to let the class use the with statement
        """
        self.close()
    
    @property
    def connection(self):
        """
        built-in function property
        """
        return self._conn

    @property
    def cursor(self):
        """
        built-in function property
        """
        return self._cursor

    def commit(self):
        """
        Commit SQL command as a transaction.
        """
        self.connection.commit()

    def close(self,commit=True):
        """
        Close the connection to db
        """
        if commit:
            self.commit()
        self._db_conn.close()

    def execute(self,sql):
        """
        Handle sql querys
        """
        self._cursor.execute(sql)