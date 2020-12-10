from glob import glob
import os
import glob
import pandas as pd
import sys
from pandas.core.series import Series

from pandas.io.stata import excessive_string_length_error


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
    def __init__(self,pfad="", suffix="xls",kriteriumIdentifikationDatei="Bewegungsdaten"): # Bewegungsdaten
        """

        """
        self._pfad = pfad
        self._suffix = suffix
        self._kriteriumIdentifikationDatei = kriteriumIdentifikationDatei
        

    def createFileList(self): 
        """
        returns list of all fileNames that contains the suffix in the tree-folders
        """
        fileList = []
        fileList = glob.glob("{0}**/*{1}?".format(self._pfad,self._suffix),recursive=True)

        return fileList

    def filterFileList(self):
        """
        input: List of files in folder-tree
        output: Filtered list of files. Condition is the file has a Sheet named = "wichtigesBlatt"
        """
        # 3) Identifiziere Tabelle "Bewegungsdaten"
        try:
            filterKriterium = self._kriteriumIdentifikationDatei
            lstAllg = self.createFileList()
            lstxls = []
            lstxlsBinary = []
            for file in lstAllg:
                if file[-1] == "b":
                    xl = pd.read_excel(file,sheet_name=None, engine='pyxlsb') # Type: Dict
                    lstWs = xl.keys()
                    dfWs = pd.DataFrame.from_dict(lstWs) # Convert to DF
                    result = dfWs.isin([filterKriterium]).any().any() & dfWs.isin(['Kopfdaten']).any().any() # Check if tableNames in df  - Returns true/false for every file
                    if result: # If tableNames exists append
                       
                        lstxlsBinary.append(file)
                        
                else:
                    xl = pd.read_excel(file,sheet_name=None) # Type: Dict
                    lstWs = xl.keys()
                    dfWs = pd.DataFrame.from_dict(lstWs) # Convert to DF                    
                    result = dfWs.isin([filterKriterium]).any().any() & dfWs.isin(['Kopfdaten']).any().any() # Check if tableNames in df - Returns true/false for every file
                    if result: # If tableNames exists append
                       
                        lstxls.append(file)

            return lstxlsBinary + lstxls   

        except ValueError as val:
            print(val)
            print("Error while returning the list.")
        
        except PermissionError as per: 
            print(per)
            print("Eine ExcelDatei ist geöffnet. Bitte schließen und neu starten.")
            sys.exit("\nSys: Programm wurde abgrochen, damit Neustart eingeleitet werden kann.")

        except Exception as e:
            print(e)
            # pass # oder sys.exc_clear()

    def excludedFiles(self):
        """

        Output: List of files with hcsr excluded
        """
        lstExcludedFiles = list(set(self.createFileList()) - set(self.filterFileList()))
        return lstExcludedFiles

    def designFilteredFileList(self):
        pass

# #########################################
# Identifikation Nicht eingeladener Dateien
# #########################################
Lister = FileList()
ergebnis = Lister.filterFileList()
print(ergebnis)

# 1) Liste Exceldateien in spezifischen Ordner - ERLEDIGT
# 2) Öffne Excel (Oder xml, csv)
# 3) Identifiziere Tabelle "Bewegungsdaten" - ERLEDIGT
# 3.1) Erstelle Liste mit HCSR Dateien
# 4) Identifiziere Überschriftenzeile 
# 5) Wenn alles vorhanden - Schreibe in liste (DB Tabelle) und übertrage in SQL DB
# 6) Wenn nicht alles vorhanden - liste Excelfiles auf bei denen es fehlt

