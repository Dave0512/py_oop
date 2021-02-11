
from typing import Dict
from openpyxl.descriptors.base import Bool
import pandas as pd
import openpyxl
from openpyxl import load_workbook
from datetime import datetime

# excelDatei = "dir_DataFrame_Center\\Test_Datumswerte_1.xlsm"

# excelBlatt = "Kopfdaten"

# excelZelle1 = "E8"
# excelZelle2 = "E10"

class ExcelTable:
    def __init__(self, dateiName,blattName):
        self._dateiName = dateiName
        self._blattName = blattName    

    def _ladeDatei(self):
        mywb = openpyxl.load_workbook(self._dateiName)
        return mywb

    def _ladeBlatt(self):
        """
        Input: openpyxl-workbook-object
        Output: openpyxl-worksheet-object
        """
        mywb = self._ladeDatei()
        myws = mywb[self._blattName]
        return myws

class XlsxDatenSauger(Dict):
    """
    Einsatz um gezielt Inhalte aus Excelzellen auszulesen
    """
    def __init__(self,blattName):
        self._dictKopfdatenCells = {"datumVon":"E8"
                            ,"datumBis":"E10"
                            ,"senderName":"E32"
                            ,"senderIdAuswahl":"E34"
                            ,"senderId":"E36"}
        self._dictKopfdatenValues = {}  
        self._blattName = blattName      

    def _erstelleZielDict(self):
        """
        Liest Zellen in ExcelBlatt und erstellt Dict mit ZellInhalt
        Input: 
            ExcelBlattName
        Output:
            Dict mit Überschrift und Inhalt aus Zellen
        """
        quellDict = self._dictKopfdatenCells   # ggfs. umbenennen
        zielDict =  self._dictKopfdatenValues # ggfs. umbenennen
        for keyval, val in quellDict.items(): # Schleife durch Dict mit Zellkennung
            inhaltAusZelle = self._blattName[val].value # Auslesen des Zellinhaltes
            zielDict[keyval] = inhaltAusZelle   
        return zielDict   # Erstellung Zieldict mit gleichen Überschriften und augelesenen Inhalten

class CompareCellValues(Bool):
    """
    Vergleiche 2 Werte.
    Konkreter Anwendungsfall: HCSR Datei Tabelle Kopfdaten enthält Beginn und Enddatum.
    """
    def __init__(self,value1,value2):
        """
        Um ein Objekt erstellen zu können müssen die beiden zu vergleichenden Werte 
        bei der Initialisierung angegeben werden.
        """
        self._value1 = value1
        self._value2 = value2
 
    def _compare(self):
        """
        Funktion um das Bool-Objekt auszugeben. 

        Der 1. Wert ist im konkrekten Anwendungsfall = Beginndate
        Einsatzgebiet: Prüfinstanz für Bestimmung valider HCSR Dateien 
        Input: 
            Zu vergleichende Zellinhalte
        Output: 
            Bool True / False (True wenn 2. Wert größer 1. Wert)
        """
        try:
            boolWert = self._value1 < self._value2
            return boolWert
        except TypeError:
            print("Fehlerhafte Formate.\nEin Vergleich kann nicht durchgeführt werden.")
            return False



# # TEST 

# initBlattObj = ExcelTable(excelDatei,excelBlatt)
# blattKopfdaten = initBlattObj._ladeBlatt()

# SaugerInitObj = XlsxDatenSauger(blattKopfdaten)
# GesaugtesDict =  SaugerInitObj._erstelleZielDict()
    
# for k, v in GesaugtesDict.items():
#     print(k,v)

# boolInit = CompareCellValues(GesaugtesDict["datumVon"],GesaugtesDict["datumBis"])
# boolTest = boolInit._compare()
# print(boolTest)
                