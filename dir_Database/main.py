from database import Database
import pyodbc

db_verb = Database("{SQL Server Native Client 11.0}"
                  ,"192.168.16.124"
                  ,"Vorlauf_DB"
                  ,"yes")

if __name__ == "__main__":
    print(type(db_verb))