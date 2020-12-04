
import pyodbc
import urllib

import sqlalchemy
from sqlalchemy import create_engine
from sqlStrings import headLieferanten
import pandas as pd
import datetime as dt

from queryTemplate import Conn_DB
from dir_Module_File_Handling.lst_fil_in_folder import FileList
from dir_DataFrame_Center.dfDesign import DfDesigner

# #################################
# 1) Liste potentielle HCSR Dateien 
# #################################

Lister = FileList()
lstHCSR = Lister.filterFileList()

# #################################
# 2) SQL Abruf
# - Abgleich Liste Dateien vs. Tabelle bereits importierter Dateien
# #################################

# #################################
# 4) Stelle Verbindung zur Db her
# #################################

datenBank = Conn_DB(driver="{SQL Server Native Client 11.0}",
                    server="192.168.16.124",
                    database="Vorlauf_DB",
                    Trusted_Connection="yes")
            
server_verbindung = datenBank.create_server_conn()



def main():
    # #################################
    # 3) Erstelle DataFrames aus identifizierten HCSR Dateien
    # #################################
    for hcsrFile in lstHCSR:
        dfHcsr = DfDesigner(fileToTransform=hcsrFile,sheetName=Lister._kriteriumIdentifikationDatei,headerCell='L_Quelle_Name*')
        realDF = dfHcsr.createFinalDf() # Erstellung modifizierter DF
        pivDF = dfHcsr._extractTables()
        # print(hcsrFile)
        # print(dfHcsr._extractTables().info())

    # #################################
    # 5) SQLImport
    # #################################
        datenBank.tblImporter(realDF,"hcsr")
        datenBank.tblImporter(pivDF,"hcsrAggr")

    
if __name__ == "__main__":
    main()




