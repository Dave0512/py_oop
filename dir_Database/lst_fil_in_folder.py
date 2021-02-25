from glob import glob
import os
import glob
import openpyxl
from openpyxl import load_workbook
import pandas as pd
import datetime as dt
import sys
from pandas.core.series import Series

from pandas.io.stata import excessive_string_length_error
# from isInCheckDf import isInChecker
from identifyCell import CellIdentifier

from openpyxlHandling import ExcelTable, XlsxDatenSauger, CompareCellValues

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


class FileList(list): # Basis
    """
    Class to identify relevant Files in Folder to transfer into Database
    List all files of a specific type 
    Input:
        path: 
        Suffix: All types possible. Default "xls"
    Output:
       list of the searched files with the given suffix

    Ex.: 
        pfad= "Z:\\1_AGKAMED_Arbeit\\0_GIT_REPOS\\1_ETL\\"
        suffix= "xls"
    """
    # Tabellen-Indentifikation: Wenn nicht Bewegungsdaten & Kopfdaten
    # Dann prüfe auf Feldnamen in allen Tabellen 'CC01_S01'
    def __init__(self,pfad="", suffix="xls",criteriasToIdentifyFile=["Bewegungsdaten","Kopfdaten"],headerCell='L_Quelle_Name*'): # Bewegungsdaten
        """
        Constructor Method
        """
        self._pfad = pfad
        self._suffix = suffix
        self._criteriasToIdentifyFile = criteriasToIdentifyFile
        self._headerCell = headerCell


    def createFileList(self): 
        """
        returns list of all fileNames that contains the suffix in the tree-folders
        """
        fileList = []
        fileList = glob.glob("{0}**/*{1}?".format(self._pfad,self._suffix),recursive=True)

        return fileList

    # def filterFileList(self):
    #     """
    #     Create a list of, which meets the following specifications:
    #         - Tables Bewegungsdaten, Kopfdaten exist
    #         - Table Kopfdaten: datumBis > datumVon
    #         - Table Bewegungsdaten: Überschrift 'L_Quelle_Name*'exists
    #     input: 
    #         List of files in folder-tree
    #     output: 
    #         Filtered list of files. Condition is the file has a Sheet named = "wichtigesBlatt"
    #     """
    #     # 3) Identify tables "Bewegungsdaten / Kopfdaten" in file
    #     try:
    #         filterKriterien = self._criteriasToIdentifyFile
    #         lstAllg = self.createFileList()
    #     except:
    #         print("Irgendwas stimmt mit den angegebenen Daten in criteriasToIdentifyFile nicht.\nOder die Gesamtliste der Dateien fehlerhaft.")
    #     else:
    #         lstxls = []
    #         lstxlsBinary = []
            
    #         for file in lstAllg:

    #             # if file[-1] == "b":
    #             #     xl = pd.read_excel(file,sheet_name=None)
    #             #     lstWs = xl.keys()
    #             #     dfWs = pd.DataFrame.from_dict(lstWs)
    #             #     wsTest = dfWs.isin([filterKriterien[0]]).any().any() & dfWs.isin([filterKriterien[1]]).any().any() # Prüfe, ob beide Tabellenblätter vorhanden
    #             #     if wsTest:
    #             #         dfData = pd.read_excel(file,sheet_name=self._criteriasToIdentifyFile[0],dtype=str,engine='pyxlsb')
    #             #         valueTest = CellIdentifier(dfData,self._headerCell)._valueExists() # Prüfe, ob 'L_Quelle_Name*' vorhanden
    #             #         if valueTest == True:
    #             #             lstxlsBinary.append(file)
    #             # else: 
    #     ## ###############################
    #     ## Prüfschritt: Tabellen vorhanden
    #     ## ###############################
    #             xl = pd.read_excel(file,sheet_name=None) # Datei in dataFrame
    #             lstWs = xl.keys() # wenn sheet_name = None, dann keys() = Tabellenblätter

    #             dfWs = pd.DataFrame.from_dict(lstWs)
    #             wsTest = dfWs.isin([filterKriterien[0]]).any().any() & dfWs.isin([filterKriterien[1]]).any().any() # Prüfe, ob beide Tabellenblätter vorhanden  
    #             if wsTest:
    #                 blattKopfdaten = ExcelTable(file,self._criteriasToIdentifyFile[1])._ladeBlatt() # Blatt "Kopfdaten" laden
    #                 gesaugtesDict = XlsxDatenSauger(blattKopfdaten)._erstelleZielDict() # Zellinhalte aus Kopfdaten laden
    #                 boolInit = CompareCellValues(gesaugtesDict["datumVon"],gesaugtesDict["datumBis"])
    #     ## ##################################
    #     ## Prüfschritt: Datumswerte Vergleich
    #     ## ##################################
    #                 datumsVgl = boolInit._compare() # Datumswerte Vergleich
    #                 if datumsVgl:
    #                     dfData = pd.read_excel(file,sheet_name=self._criteriasToIdentifyFile[0],dtype=str)
    #     ## #################################################
    #     ## Prüfschritt: Prüfe, ob 'L_Quelle_Name*' vorhanden
    #     ## #################################################
    #                     valueTest = CellIdentifier(dfData,self._headerCell)._valueExists() 
    #                     if valueTest == True:
    #                         lstxls.append(file) 

    #         return lstxlsBinary + lstxls

    
    # # ###################################################
    # # Überführung def filterFileList in einzelne Schritte
    # # ###################################################
    
    ## ##################################
    ## 1) Prüfschritt: Tabellen vorhanden
    ## ##################################
    def _filterTabs(self):
        try:
            filterKriterien = self._criteriasToIdentifyFile
            lstAllg = self.createFileList()
        except:
            print("Irgendwas stimmt mit den angegebenen Daten in criteriasToIdentifyFile nicht.\nOder die Gesamtliste der Dateien fehlerhaft.")
        else:
            lstTabsOk = []
            lstTabsError = []
            
            for file in lstAllg:
                xl = pd.read_excel(file,sheet_name=None) # Datei in dataFrame
                lstWs = xl.keys() # wenn sheet_name = None, dann keys() = Tabellenblätter

                dfWs = pd.DataFrame.from_dict(lstWs)
                wsTest = dfWs.isin([filterKriterien[0]]).any().any() & dfWs.isin([filterKriterien[1]]).any().any() # Prüfe, ob beide Tabellenblätter vorhanden  
                if wsTest == True:
                    lstTabsOk.append(file)

                else:
                    lstTabsError.append(file)
                
            return lstTabsOk, lstTabsError 
    ## #####################################
    ## 2) Prüfschritt: Datumswerte Vergleich
    ## #####################################
    def _filterDatumsWerte(self):
        lstTabsOk = self._filterTabs()[0]
        lstDatOk = []
        lstDatError = []
        for file in lstTabsOk:
            blattKopfdaten = ExcelTable(file,self._criteriasToIdentifyFile[1])._ladeBlatt() # Blatt "Kopfdaten" laden
            gesaugtesDict = XlsxDatenSauger(blattKopfdaten)._erstelleZielDict() # Zellinhalte aus Kopfdaten laden
            boolInit = CompareCellValues(gesaugtesDict["datumVon"],gesaugtesDict["datumBis"])

            datumsVgl = boolInit._compare() # Datumswerte Vergleich
            if datumsVgl:
                lstDatOk.append(file)
            else:
                lstDatError.append(file)

        return lstDatOk, lstDatError

    ## ####################################################
    ## 3) Prüfschritt: Prüfe, ob 'L_Quelle_Name*' vorhanden
    ## ####################################################
    def _filterUeberschriften(self):
        lstDatOk = self._filterDatumsWerte()[0]
        lstUebOk = []
        lstUebError = []

        for file in lstDatOk:
            dfData = pd.read_excel(file,sheet_name=self._criteriasToIdentifyFile[0],dtype=str)
            valueTest = CellIdentifier(dfData,self._headerCell)._valueExists() 
            if valueTest == True:
                lstUebOk.append(file)   
            else:
                lstUebError.append(file)

        return lstUebOk, lstUebError 

    def _gefilterte_hcsr_liste_uebergeben(self):
        lst_hcsr_final = self._filterUeberschriften()[0]
        return lst_hcsr_final
        
        # except ValueError as val:
        #     return "Error while returning the list."
        
        # except PermissionError as per: 
        #     print(per)
        #     print("Eine ExcelDatei ist geöffnet. Bitte schließen und neu starten.")
        #     sys.exit("\nSys: Programm wurde abgrochen, damit Neustart eingeleitet werden kann.")

        # except Exception as e:
        #     print(e)
        #     # pass # oder sys.exc_clear()

    # def excludedFiles(self):
    #     """

    #     Output: List of files with hcsr excluded
    #     """
    #     lstExcludedFiles = list(set(self.createFileList()) - set(self.filterFileList()))
    #     if lstExcludedFiles:
    #         return lstExcludedFiles
    #     else:
    #         print("Liste ist leer, da keine \nfehlerhaften Dateien vorhanden sind.")

    def designFilteredFileList(self):
        pass

# #########################################
# Identifikation Nicht eingeladener Dateien
# #########################################
# Lister = FileList()

# # # TEST 1
# ergebnis1 = Lister._filterTabs()
# ergebnis1TabsOk = ergebnis1[0]
# ergebnis1TabsAusgeschl = ergebnis1[1]

# print(type(ergebnis1))
# print(type(ergebnis1TabsOk))
# print(ergebnis1TabsOk)

# print(type(ergebnis1TabsAusgeschl))
# print(ergebnis1TabsAusgeschl)

# # Test 2
# ergebnis2 = Lister._filterDatumsWerte()
# print(ergebnis2)


# ergebnisAusschluss = Lister.excludedFiles()
# print(ergebnisAusschluss)

# 1) Liste Exceldateien in spezifischen Ordner - ERLEDIGT
# 2) Öffne Excel (Oder xml, csv)
# 3) Identifiziere Tabelle "Bewegungsdaten" - ERLEDIGT
# 3.1) Erstelle Liste mit HCSR Dateien
# 4) Identifiziere Überschriftenzeile 
# 5) Wenn alles vorhanden - Schreibe in liste (DB Tabelle) und übertrage in SQL DB
# 6) Wenn nicht alles vorhanden - liste Excelfiles auf bei denen es fehlt

