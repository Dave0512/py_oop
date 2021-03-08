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
    #         return lstxlsBinary + lstxls

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
                # if file[-1] != "b":
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
            # if file[-1] != "b":
            dfData = pd.read_excel(file,sheet_name=self._criteriasToIdentifyFile[0],dtype=str)
            valueTest = CellIdentifier(dfData,self._headerCell)._lstValuesExists()
            if valueTest == True:
                lstUebOk.append(file)   
            else:
                lstUebError.append(file)

        return lstUebOk, lstUebError 

    def _filterUstID(self):
        lstUebOk = self._filterUeberschriften()[0]
        lstUstIDOk = []
        lstUstIDError = []   

        for file in lstUebOk:
            blattKopfdaten = ExcelTable(file,self._criteriasToIdentifyFile[1])._ladeBlatt() # Blatt "Kopfdaten" laden
            gesaugtesDict = XlsxDatenSauger(blattKopfdaten)._erstelleZielDict() # Zellinhalte aus Kopfdaten laden
            USTID_Test = gesaugtesDict["senderId"]
            if USTID_Test == "USTID":
                lstUstIDOk.append(file)
            else:
                lstUstIDError.append(file)
        
        return lstUstIDOk, lstUstIDError

    def _gefilterte_hcsr_liste_uebergeben(self):
        # lst_hcsr_final = self._filterUeberschriften()[0]
        lst_hcsr_final = self._filterUstID()[0]
        return lst_hcsr_final

