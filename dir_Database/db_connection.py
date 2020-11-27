

from sqlalchemy import create_engine
import sqlalchemy
import urllib

print(help(create_engine))

class DB_Connect:
    """
    Datenbank Connector Klasse (sqlalchemy)
    Instanz der Klasse dient als Verbindung zur Datenbank
    """
    
    db_conn_string = urllib.parse.quote_plus(r"DRIVER={SQL Server Native Client 11.0};"
                                            r"SERVER=192.168.16.124;"
                                            r"DATABASE=Vorlauf_DB;"
                                            r"Trusted_Connection=yes;")

    server_verbindung = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect={}".format(db_conn_string))
    return server_verbindung




