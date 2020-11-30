from database import Database
import pyodbc
import urllib
from queryTemplate import Conn_DB
import sqlalchemy
from sqlalchemy import create_engine
from sqlStrings import headLieferanten
import pandas as pd

datenBank = Conn_DB(driver="{SQL Server Native Client 11.0}",
                    server="192.168.16.124",
                    database="Vorlauf_DB",
                    Trusted_Connection="yes")
            
server_verbindung = datenBank.create_server_conn()

def main():
    
    print(datenBank.sqlExecuter)
    print(isinstance(datenBank.create_server_conn(),sqlalchemy.engine.base.Connection))
    
    resultsqlExecuter = datenBank.sqlExecuter(headLieferanten)
    print(resultsqlExecuter.fetchall())

    df_hcsr = pd.read_excel('01_2020_Health Care Sales Report V2.1_Abbott Medical_AGKAMED.xlsm'
                       ,sheet_name='Bewegungsdaten',dtype=str)
    
    for row in range(df_hcsr.shape[0]): 
        for col in range(df_hcsr.shape[1]):
            if df_hcsr.iat[row,col] == 'L_Quelle_Name*':
                row_start = row
                break

    new_header = df_hcsr.iloc[row_start] #grab the first row for the header
    df_hcsr = df_hcsr[1:] #take the data less the header row
    df_hcsr.columns = new_header #set the header row as the df header
    df_hcsr = df_hcsr.rename(columns = {c: c.replace('*','_MUSS_FELD_') for c in df_hcsr.columns})
    df_hcsr.to_sql("hcsr",con=server_verbindung,if_exists='append',index=False)
    
if __name__ == "__main__":
    main()




