
import pyodbc
import urllib

import sqlalchemy
from sqlalchemy import create_engine
from sqlStrings import headLieferanten, sql_stored_proc_add_prio_flag, sql_add_prio_flag_gesamt, sql_add_prio_flag_part_final, sql_gui_tab_hcsr_import_erfolgreich_2, sql_gui_tab_hcsr_import_fehlerhaft, sql_add_prio_flag_part_1,  sql_add_prio_flag_part_4 # sql_add_prio_flag_part_2, sql_add_prio_flag_part_3,
import pandas as pd
import datetime as dt

from queryTemplate import Conn_DB
from lst_fil_in_folder import FileList
from dfDesign import TableToDF, DfDesignerPiv, DFDesignerDistinctFiles
from dfFromList import ListToDF
from openpyxlHandling import ExcelTable, XlsxDatenSauger
from queryTemplate_pyodbc import Conn_DB_by_pyodbc
import pyodbc

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# #################################
# 2) SQL Abruf
# - Abgleich Liste Dateien vs. Tabelle bereits importierter Dateien
# #################################

def verbinde_zu_server_und_db():
    with pyodbc.connect(r"DRIVER={SQL Server Native Client 11.0};"
                                "SERVER=192.168.16.124;"
                                "DATABASE=Vorlauf_DB;"
                                "Trusted_Connection=yes;") as verb_db:

        return verb_db

def sql_executer(sql_string):
    db_verb = verbinde_zu_server_und_db()
    cur = db_verb.cursor()
    cur.execute(sql_string)
    db_verb.commit()

# #################################
# 4) Stelle Verbindung zur Db her
# #################################



datenBank = Conn_DB(driver="{SQL Server Native Client 11.0}",
                    server="192.168.16.124",
                    database="Vorlauf_DB",
                    Trusted_Connection="yes")

server_verbindung = datenBank.create_server_conn()
def ausfuehren():
    # aufbauDatenbankMitAbhängigkeiten = datenBank.sqlExecuter(sql_datenModell) 
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
    index_count=0 
    for hcsrFile in lstHCSR:
        index_count += 1
        fileToTransform=hcsrFile
        headerCell='L_Quelle_Name*'
        # # BaseClass
        dfHcsr = TableToDF(fileToTransform=fileToTransform,sheetName=sheetName,headerCell=headerCell)
        realDF = dfHcsr._createFinalDf() # Erstellung modifizierter DF
        realDF['datei_id_counter'] = index_count
        # realDF['_DateiNameCompKey_'] = realDF['_DateiName_'].astype(str)+ "°" +  realDF['datei_id_counter'] + "°" + realDF['_date_inload_minute_'].astype(str)
        # realDF['_date_inload_minute_2'] = dt.datetime.now().isoformat(' ', 'minutes')

        # # Inheritance
        dfCoreErbe = DfDesignerPiv(fileToTransform=fileToTransform,sheetName=sheetName,headerCell=headerCell)
        DFErbe = dfCoreErbe._extractTables()
        DFErbe['datei_id_counter'] = index_count
        # DFErbe['_DateiNameCompKey_'] = DFErbe['_DateiName_'].astype(str)+ "°" +  DFErbe['datei_id_counter'] + "°" + DFErbe['_date_inload_minute_'].astype(str)

        # # HCSR Dateien inkl. Inload Datum = Identifikation Datei + Übertrag in tab hcsrFiles 
        dfCoreErbeDistinctFiles = DFDesignerDistinctFiles(fileToTransform=fileToTransform,sheetName=sheetName,headerCell=headerCell)
        dfErbeDistinctFiles = dfCoreErbeDistinctFiles._extractTables()
        dfErbeDistinctFiles['datei_id_counter'] = index_count
        # dfErbeDistinctFiles['_DateiNameCompKey_'] = dfErbeDistinctFiles['_DateiName_'].astype(str)+ "°" +  dfErbeDistinctFiles['datei_id_counter'] + "°" + dfErbeDistinctFiles['_date_inload_minute_'].astype(str)        
        
        blattKopfdaten = ExcelTable(hcsrFile,Lister._criteriasToIdentifyFile[1])._ladeBlatt() # Blatt "Kopfdaten" laden
        gesaugtesDict = XlsxDatenSauger(blattKopfdaten)._erstelleZielDict() # Zellinhalte aus Kopfdaten laden
        gesaugtesDf = pd.DataFrame(gesaugtesDict, index=[0])
        gesaugtesDf['_date_inload_'] = dt.datetime.now()
        gesaugtesDf['_date_inload_minute_'] = dt.datetime.now().isoformat(' ', 'minutes')
        gesaugtesDf['_date_inload_hour_'] = dt.datetime.now().isoformat(' ', 'hours')
        gesaugtesDf['_DateiName_'] = hcsrFile.split("\\")[-1] 

        gesaugtesDf['_LieferantCompKey_'] = gesaugtesDf['senderId'].astype(str) + "°" + gesaugtesDf['datumVon'].astype(str) + "°" + gesaugtesDf['datumBis'].astype(str)                                
        gesaugtesDf['datei_id_counter'] = index_count
        # gesaugtesDf['_DateiNameCompKey_'] = gesaugtesDf['_DateiName_'].astype(str)+ "°" +  gesaugtesDf['datei_id_counter'] + "°" + gesaugtesDf['_date_inload_minute_'].astype(str)
        gesaugtesDf['_DateiNameCompKey_'] = gesaugtesDf['_DateiName_'].astype(str)+ "°" + gesaugtesDf['_date_inload_minute_'].astype(str)
        dfKopfdatenValues = dfKopfdatenValues.append(gesaugtesDf,ignore_index=True)


# #################################
# 5) SQLImport
# #################################
        datenBank.tblImporter(dfErbeDistinctFiles,"hcsrFiles")  
        datenBank.tblImporter(realDF,"hcsr")
        datenBank.tblImporter(DFErbe,"hcsrAggr")
    datenBank.tblImporter(dfKopfdatenValues,"hcsrKopfdaten")
        
    dfCoreExcluded = ListToDF()
    dfExcluded = dfCoreExcluded._extractTables()
    datenBank.tblImporter(dfExcluded,"hcsrFilesExcluded")

    sql_executer(sql_add_prio_flag_gesamt)

# # Datenbank Manipulation über SQL-Querys
# def sqlQueries():
#     datenBank.sqlExecuter(sql_stored_proc_add_prio_flag)
#     # datenBank.sqlExecuterMany(sql_add_prio_flag_gesamt)



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
        df_of_resultproxy = datenBank.sqlExecuterResultProxyToDF(sql_gui_tab_hcsr_import_erfolgreich_2)
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
