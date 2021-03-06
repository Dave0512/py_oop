
import sqlalchemy
from sqlalchemy import create_engine
import urllib


class Conn_DB:
    """
    Choose DB Connection-Framework 
    Choose between different Dialects, will be implemented
    """
    def __init__(self,db_conn_lib="sqlalchemy",driver="",server="",database="",Trusted_Connection=""):
        """
        Library festlegen
        Ex.: 
            pyodbc, sqlalchemy
        """
        self.db_conn_lib = db_conn_lib
        self._driver = driver
        self._server = server
        self._database = database
        self._Trusted_Connection = Trusted_Connection
        # self._relevanteFiles = 
  

    def design_login_string(self): 
        """

        Ex.:
              login_string = urllib.parse.quote_plus(
                                 r"DRIVER={SQL Server Native Client 11.0};"
                                 r"SERVER=192.168.16.124;"
                                 r"DATABASE=Vorlauf_DB;"
                                 r"Trusted_Connection=yes;")   
        """ 
        login_string = urllib.parse.quote_plus(r"DRIVER={};"
                                               r"SERVER={};"
                                               r"DATABASE={};"
                                               r"Trusted_Connection={};".format(self._driver
                                                                                ,self._server
                                                                                ,self._database
                                                                                ,self._Trusted_Connection))   
        return login_string

    def create_server_conn(self):
        """
        Create SQLAlchemy Engine 
        """
        server_login = self.design_login_string()
        server_engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect={}".format(server_login))    
        server_verbindung = server_engine.connect()
        return server_verbindung

    def sqlExecuter(self,sqlString):
        """
        Run SQL Querys 
        """
        dbVerb = self.create_server_conn()
        sqlExecution = dbVerb.execute(sqlString)
        return sqlExecution

    def tblImporter(self,tblDataFrame,tableName="hcsr"):
        if tblDataFrame is not None:       
            tblDataFrame.to_sql(tableName,con=self.create_server_conn(),if_exists='append',index=False)
        else:
            print(str(tableName) + " ist leer. Hier wird nichts in die Datenbank übergeben.")


# #######################################################################################################################

class QueryTemplate:
    """
    Class to interact with databases
    """
    
    def __init__(self, *args):
        DB_Connector = Conn_DB()
        _datenbankVerbindung = DB_Connector.create_server_conn()

    # def connect(self):

        # if isinstance(self._verbindungsAufbau,sqlalchemy.engine.base.Connection) == True:
            # pass

    def tblImporter(self,tblDataFrame,tableName="hcsr"):
        pass
        
    def construct_query(self):
        pass

    def do_query(self):
        pass

    def format_results(self):
        pass

    def output_results(self):
        pass

    def process_format(self):
        """
        Sequence control of the functions 
        - The process_format method is the primary method to be called by an outside
          client. 
        - It ensures each step is executed in order, but it does not care if that step is
          implemented in this class or in a subclass.
        """
        self.connect()
        self.construct_query()
        self.do_query()
        self.format_results()
        self.output_results()
        
        
        
        

        

        