from glob import glob
import os
import glob
import pandas as pd
import sys


class FileList(list):
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
    
    def __init__(self,pfad="", suffix="xls",kriteriumIdentifikationDatei="Bewegungsdaten"):
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
                    xl = pd.read_excel(file,sheet_name=None, engine='pyxlsb')
                    lstWs = xl.keys()
                    for sheet in lstWs:
                        if str(sheet) == filterKriterium:
                            lstxlsBinary.append(file)

                else:
                    xl = pd.read_excel(file,sheet_name=None)
                    lstWs = xl.keys()
                    for sheet in lstWs:
                        if str(sheet) == filterKriterium:
                            lstxls.append(file)

            return lstxlsBinary + lstxls   
        except ValueError as val:
            print(val)
            print("Error with returning the list.")
        
        except PermissionError as per: 
            print(per)
            print("Eine ExcelDatei ist geöffnet. Bitte schließen und neu starten.")
            sys.exit("\nSys: Programm wurde abgrochen, damit Neustart eingeleitet werden kann.")

        except Exception as e:
            print(e)
            pass # oder sys.exc_clear()


    def designFilteredFileList(self):
        pass


# Lister = FileList()
# ergebnis = Lister.filterFileList()

# print(ergebnis)

# 1) Liste Exceldateien in spezifischen Ordner - ERLEDIGT
# 2) Öffne Excel (Oder xml, csv)
# 3) Identifiziere Tabelle "Bewegungsdaten" - ERLEDIGT
# 3.1) Erstelle Liste mit HCSR Dateien
# 4) Identifiziere Überschriftenzeile 
# 5) Wenn alles vorhanden - Schreibe in liste (DB Tabelle) und übertrage in SQL DB
# 6) Wenn nicht alles vorhanden - liste Excelfiles auf bei denen es fehlt

