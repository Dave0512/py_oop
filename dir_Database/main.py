
import pyodbc
import urllib

import sqlalchemy
from sqlalchemy import create_engine
from sqlStrings import headLieferanten, sql_gui_tab_hcsr_import_erfolgreich
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
# print(len(lstHCSR)) # Alle Dateien
# print(len(Lister.createFileList())) # Alle Dateien die eingespielt werden

# fehlerhafteDateien = list(set(Lister.createFileList()) - set(lstHCSR))
# for file in fehlerhafteDateien: # Ausgeschlossene Dateien
#     print(file)


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

# SQlAusf = datenBank.sqlExecuter(sql_gui_tab_hcsr_import_erfolgreich)



def ausfuehren():
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

# ######################################
# Entgegennahme der SQL Query Ergebnisse
# ######################################

# 1 Funktion je QueryErgebnis 
# Aktuell für Übergabe an GUI Tabellen

def dfFromSQLHcsrFilesImported():
    """
    Recieves SQLAlchemy ResultProxy Object of SQL Query
    Input: 
        ResultProxy Object (SQl Query) in dict / list-format
    Output:
        Pandas DataFrame of the sql-query results
    """
    df_of_resultproxy = datenBank.sqlExecuterResultProxyToDF(sql_gui_tab_hcsr_import_erfolgreich)
    return df_of_resultproxy


# print(type(datenBank.create_cursor()))


# # Test: Als DF formatiertes Query Ergebnis 
# df = dfFromSQLHcsrFilesImported()
# print(type(dfFromSQLHcsrFilesImported()))





