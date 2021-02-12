from glob import glob
import os
import glob
import pandas as pd
import sys
from pandas.core.series import Series

from pandas.io.stata import excessive_string_length_error
# from isInCheckDf import isInChecker
from identifyCell import CellIdentifier

from openpyxlHandling import ExcelTable, XlsxDatenSauger, CompareCellValues


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

    def filterFileList(self):
        """
        Create a list of, which meets the following specifications:
            - Tables Bewegungsdaten, Kopfdaten exist
            - Table Kopfdaten: datumBis > datumVon
            - Table Bewegungsdaten: Überschrift 'L_Quelle_Name*'exists
        input: 
            List of files in folder-tree
        output: 
            Filtered list of files. Condition is the file has a Sheet named = "wichtigesBlatt"
        """
        # 3) Identify tables "Bewegungsdaten / Kopfdaten" in file
        try:
            filterKriterien = self._criteriasToIdentifyFile
            lstAllg = self.createFileList()
        except:
            print("Irgendwas stimmt mit den angegebenen Daten in criteriasToIdentifyFile nicht.\nOder die Gesamtliste der Dateien fehlerhaft.")
        else:
            lstxls = []
            lstxlsBinary = []
            
            for file in lstAllg:
                initBlattObj = ExcelTable(file,self._criteriasToIdentifyFile[1])
                blattKopfdaten = initBlattObj._ladeBlatt()

                SaugerInitObj = XlsxDatenSauger(blattKopfdaten)
                gesaugtesDict =  SaugerInitObj._erstelleZielDict()
        
                boolInit = CompareCellValues(gesaugtesDict["datumVon"],gesaugtesDict["datumBis"])
                boolTest = boolInit._compare()
                # if file[-1] == "b":
                #     xl = pd.read_excel(file,sheet_name=None)
                #     lstWs = xl.keys()
                #     dfWs = pd.DataFrame.from_dict(lstWs)
                #     wsTest = dfWs.isin([filterKriterien[0]]).any().any() & dfWs.isin([filterKriterien[1]]).any().any() # Prüfe, ob beide Tabellenblätter vorhanden
                #     if wsTest:
                #         dfData = pd.read_excel(file,sheet_name=self._criteriasToIdentifyFile[0],dtype=str,engine='pyxlsb')
                #         valueTest = CellIdentifier(dfData,self._headerCell)._valueExists() # Prüfe, ob 'L_Quelle_Name*' vorhanden
                #         if valueTest == True:
                #             lstxlsBinary.append(file)
                # else: 
                xl = pd.read_excel(file,sheet_name=None)
                lstWs = xl.keys()
                dfWs = pd.DataFrame.from_dict(lstWs)
                wsTest = dfWs.isin([filterKriterien[0]]).any().any() & dfWs.isin([filterKriterien[1]]).any().any() & boolTest # Prüfe, ob beide Tabellenblätter vorhanden
                if wsTest:
                    dfData = pd.read_excel(file,sheet_name=self._criteriasToIdentifyFile[0],dtype=str)
                    valueTest = CellIdentifier(dfData,self._headerCell)._valueExists() # Prüfe, ob 'L_Quelle_Name*' vorhanden
                    if valueTest == True:
                        lstxls.append(file) 
                        print(file)
                        gesaugtesDf = pd.DataFrame(gesaugtesDict, index=[0])
                        print(gesaugtesDf.head())
                        # for k, v in GesaugtesDict.items():
                        #     print(k,v)
            return lstxlsBinary + lstxls  


        # except ValueError as val:
        #     return "Error while returning the list."
        
        # except PermissionError as per: 
        #     print(per)
        #     print("Eine ExcelDatei ist geöffnet. Bitte schließen und neu starten.")
        #     sys.exit("\nSys: Programm wurde abgrochen, damit Neustart eingeleitet werden kann.")

        # except Exception as e:
        #     print(e)
        #     # pass # oder sys.exc_clear()

    def excludedFiles(self):
        """

        Output: List of files with hcsr excluded
        """
        lstExcludedFiles = list(set(self.createFileList()) - set(self.filterFileList()))
        if lstExcludedFiles:
            return lstExcludedFiles
        else:
            print("Liste ist leer, da keine \nfehlerhaften Dateien vorhanden sind.")

    def designFilteredFileList(self):
        pass

# #########################################
# Identifikation Nicht eingeladener Dateien
# #########################################
Lister = FileList()
ergebnis = Lister.filterFileList()
print(ergebnis)

# ergebnisAusschluss = Lister.excludedFiles()
# print(ergebnisAusschluss)

# 1) Liste Exceldateien in spezifischen Ordner - ERLEDIGT
# 2) Öffne Excel (Oder xml, csv)
# 3) Identifiziere Tabelle "Bewegungsdaten" - ERLEDIGT
# 3.1) Erstelle Liste mit HCSR Dateien
# 4) Identifiziere Überschriftenzeile 
# 5) Wenn alles vorhanden - Schreibe in liste (DB Tabelle) und übertrage in SQL DB
# 6) Wenn nicht alles vorhanden - liste Excelfiles auf bei denen es fehlt

