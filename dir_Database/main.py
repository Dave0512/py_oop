
import pyodbc
import urllib

import sqlalchemy
from sqlalchemy import create_engine
from sqlStrings import headLieferanten, sql_gui_tab_hcsr_import_erfolgreich, sql_gui_tab_hcsr_import_fehlerhaft
import pandas as pd
import datetime as dt

from queryTemplate import Conn_DB
from lst_fil_in_folder import FileList
from dfDesign import TableToDF, DfDesignerPiv
from dfFromList import ListToDF
from openpyxlHandling import ExcelTable, XlsxDatenSauger

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

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

def ausfuehren():

    # #################################
    # 1) Liste potentielle HCSR Dateien
    # #################################

    Lister = FileList()
    lstHCSR = Lister._gefilterte_hcsr_liste_uebergeben() # Ersetzt Lister.filterFileList()

    # #################################
    # 3) Erstelle DataFrames aus identifizierten HCSR Dateien
    # #################################
    sheetName=Lister._criteriasToIdentifyFile[0]

    dfKopfdatenValues = pd.DataFrame()
    for hcsrFile in lstHCSR:
        fileToTransform=hcsrFile
        headerCell='L_Quelle_Name*'
        # # BaseClass
        dfHcsr = TableToDF(fileToTransform=fileToTransform,sheetName=sheetName,headerCell=headerCell)
        realDF = dfHcsr._createFinalDf() # Erstellung modifizierter DF

        # # Inheritance
        dfCoreErbe = DfDesignerPiv(fileToTransform=fileToTransform,sheetName=sheetName,headerCell=headerCell)
        DFErbe = dfCoreErbe._extractTables()

        blattKopfdaten = ExcelTable(hcsrFile,Lister._criteriasToIdentifyFile[1])._ladeBlatt() # Blatt "Kopfdaten" laden
        gesaugtesDict = XlsxDatenSauger(blattKopfdaten)._erstelleZielDict() # Zellinhalte aus Kopfdaten laden
        gesaugtesDf = pd.DataFrame(gesaugtesDict, index=[0])
        gesaugtesDf['_date_inload_'] = dt.datetime.now()
        gesaugtesDf['_DateiName_'] = hcsrFile.split("\\")[-1]
        gesaugtesDf['_LieferantCompKey_'] = gesaugtesDf['senderId'].astype(str) + "°" + gesaugtesDf['datumVon'].astype(str) + "°" + gesaugtesDf['datumBis'].astype(str)                                
        gesaugtesDf['_DateiNameCompKey_'] = gesaugtesDf['_DateiName_'].astype(str) + "°" + gesaugtesDf['_date_inload_'].astype(str)
        dfKopfdatenValues = dfKopfdatenValues.append(gesaugtesDf,ignore_index=True)

# #################################
# 5) SQLImport
# #################################
        datenBank.tblImporter(realDF,"hcsr")
        datenBank.tblImporter(DFErbe,"hcsrAggr")
        datenBank.tblImporter(dfKopfdatenValues,"hcsrKopfdaten")

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
    try:
        df_of_resultproxy = datenBank.sqlExecuterResultProxyToDF(sql_gui_tab_hcsr_import_erfolgreich)
    except AttributeError:
        print("Tabelle nicht vorhanden - in MAIN Funktion aufgerufen")
    else:
        return df_of_resultproxy

def dfFromSQLHcsrFilesError():
    """
    Recieves SQLAlchemy ResultProxy Object of SQL Query
    Input: 
        ResultProxy Object (SQl Query) in dict / list-format
    Output: 
        Pandas DataFrame of the sql-query results
    """
    try:
        df_of_resultproxy = datenBank.sqlExecuterResultProxyToDF(sql_gui_tab_hcsr_import_fehlerhaft)
    except AttributeError:
        print("Tabelle nicht vorhanden - in MAIN Funktion aufgerufen")
    else:
        return df_of_resultproxy
