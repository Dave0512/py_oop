
import pyodbc
import urllib

import sqlalchemy
from sqlalchemy import create_engine
from sqlStrings import headLieferanten
import pandas as pd
import datetime as dt

from queryTemplate import Conn_DB
from lst_fil_in_folder import FileList
from dfDesign import TableToDF, DfDesignerPiv
from dfFromList import ListToDF

# #################################
# 1) Liste potentielle HCSR Dateien 
# #################################

Lister = FileList()
lstHCSR = Lister.filterFileList()
print(len(lstHCSR))
print(len(Lister.createFileList()))

fehlerhafteDateien = list(set(Lister.createFileList()) - set(lstHCSR))
print(fehlerhafteDateien)


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
    sheetName=Lister._criteriasToIdentifyFile[0]
    

    for hcsrFile in lstHCSR:
        fileToTransform=hcsrFile
        headerCell='L_Quelle_Name*'
        # # BaseClass
        dfHcsr = TableToDF(fileToTransform=fileToTransform,sheetName=sheetName,headerCell=headerCell)
        realDF = dfHcsr._createFinalDf() # Erstellung modifizierter DF
        
        # # Inheritance
        dfCoreErbe = DfDesignerPiv(fileToTransform=fileToTransform,sheetName=sheetName,headerCell=headerCell)
        DFErbe = dfCoreErbe._extractTables()
        # print(hcsrFile)
        # print(dfHcsr._extractTables().info())

    

    # #################################
    # 5) SQLImport
    # #################################
        datenBank.tblImporter(realDF,"hcsr")
        datenBank.tblImporter(DFErbe,"hcsrAggr")

dfCoreExcluded = ListToDF()
dfExcluded = dfCoreExcluded._extractTables()

datenBank.tblImporter(dfExcluded,"hcsrFilesExcluded")
    
    
if __name__ == "__main__":
    main()




