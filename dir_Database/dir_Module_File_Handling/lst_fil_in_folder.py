from glob import glob
import os
import glob
import pandas as pd


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

    def createFileList(self): # , tableName, headerCell):
        """
        returns list of all fileNames that contains the suffix in the tree-folders
        """
        fileList = []
        fileList = glob.glob("{0}**/*{1}*".format(self._pfad,self._suffix),recursive=True)
        return fileList

    def filterFileList(self):
        """
        input: List of files in folder-tree
        output: Filtered list of files. Condition is the file has a Sheet named = "wichtigesBlatt"
        """
        # 3) Identifiziere Tabelle "Bewegungsdaten"
        filterKriterium = self._kriteriumIdentifikationDatei
        lstAllg = self.createFileList()
        lstHCSRFiles = []
        for file in lstAllg:
            xl = pd.ExcelFile(file) 

            lstWs = xl.sheet_names
            for sheet in lstWs:
                if str(sheet) == filterKriterium:
                    lstHCSRFiles.append(file.split("\\")[-1])  
        
        return lstHCSRFiles

    def designFilteredFileList(self):
        pass
        # lstFilt = filterFileList



# 1) Liste Exceldateien in spezifischen Ordner - ERLEDIGT
# 2) Öffne Excel (Oder xml, csv)
# 3) Identifiziere Tabelle "Bewegungsdaten" - ERLEDIGT
# 3.1) Erstelle Liste mit HCSR Dateien
# 4) Identifiziere Überschriftenzeile 
# 5) Wenn alles vorhanden - Schreibe in liste (DB Tabelle) und übertrage in SQL DB
# 6) Wenn nicht alles vorhanden - liste Excelfiles auf bei denen es fehlt

