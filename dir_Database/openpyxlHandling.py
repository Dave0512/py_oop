
from openpyxl.descriptors.base import Bool
import pandas as pd
import openpyxl
from openpyxl import load_workbook
from datetime import datetime

excelDatei = "dir_DataFrame_Center\\01_2020_Health Care Sales Report V2.1_Abbott Medical_AGKAMED.xlsm"

excelBlatt = "Kopfdaten"

excelZelle1 = "E8"
excelZelle2 = "E10"


class CellValueFromExcel:
    """
    Class to extract Cell Values from an excelfile, excelsheet
    Based on openpyxl module to handle excel sheets
    """
    def __init__(self, dateiName,blattName,zelle):
        self._dateiName = dateiName
        self._blattName = blattName
        self._zelle = zelle
    
    def _ladeDatei(self):
        mywb = openpyxl.load_workbook(self._dateiName)
        return mywb

    def _ladeBlatt(self):
        mywb = self._ladeDatei()
        myws = mywb[self._blattName]
        return myws

    def _zelleAuslesen(self):
        myws = self._ladeBlatt()
        myCell = myws[self._zelle]
        myCellValue = myCell.value
        return myCellValue


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
            if self._value1 < self._value2:
                return True
        except TypeError:
                return "Fehlerhafte Formate.\nKann nicht berechnet werden."
        finally:
            return False


# # TEST 
zelleInWb = CellValueFromExcel(excelDatei,excelBlatt,excelZelle1)
ausgelesenerZellWert1 = zelleInWb._zelleAuslesen()

zelleInWb = CellValueFromExcel(excelDatei,excelBlatt,excelZelle2)
ausgelesenerZellWert2 = zelleInWb._zelleAuslesen()

print(ausgelesenerZellWert1)
print(ausgelesenerZellWert2)

boolTestObj = CompareCellValues(ausgelesenerZellWert1,ausgelesenerZellWert2)
test = boolTestObj._compare()
print(test)
                