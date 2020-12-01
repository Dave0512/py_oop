from glob import glob
import os
import glob


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
    
    def __init__(self,pfad="", suffix="xls"):
        """

        """
        self._pfad = pfad
        self._suffix = suffix

    def searchFile(self): # , tableName, headerCell):
        """
        returns all fileNames that contains the suffix, tableName and headerCell
        """
        fileList = []
        fileList = glob.glob("{0}**/*{1}*".format(self._pfad,self._suffix),recursive=True)
        return fileList


# Test 
Lister = FileList("Z:\\1_AGKAMED_Arbeit\\0_GIT_REPOS\\1_ETL\\","ipynb")

print(Lister.searchFile())

# 1) Liste Exceldateien in spezifischen Ordner 
# 2) Öffne Excel (Oder xml, csv)
# 3) Identifiziere Tabelle "Bewegungsdaten"
# 4) Identifiziere Überschriftenzeile
# 5) Wenn alles vorhanden - Schreibe in liste (DB Tabelle) und übertrage in SQL DB
# 6) Wenn nicht alles vorhanden - liste Excelfiles auf bei denen es fehlt

