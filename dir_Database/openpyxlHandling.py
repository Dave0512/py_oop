
from openpyxl.descriptors.base import Bool
import pandas as pd
import openpyxl
from openpyxl import load_workbook
from datetime import datetime

excelDatei = "dir_DataFrame_Center\\Test_Datumswerte_1.xlsm"

excelBlatt = "Kopfdaten"

excelZelle1 = "E8"
excelZelle2 = "E10"


class ExcelTable:
    def __init__(self, dateiName,blattName):
        self._dateiName = dateiName
        self._blattName = blattName
        self._dictKopfdatenCells = {"datumVon":"E8"
                            ,"datumBis":"E10"
                            ,"senderName":"E32"
                            ,"senderIdAuswahl":"E34"
                            ,"senderId":"E36"}
        self._dictKopfdatenValues = {}        

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

class CellValueFromExcel:
    """
    Class to extract Cell Values from an excelfile, excelsheet
    Based on openpyxl module to handle excel sheets
    """
    def __init__(self, blattName,zelle):
        self._blattName = blattName
        self._zelle = zelle

    def _einzelneZelleAuslesen(self):
        """
        Input: openpyxl-worksheet-object
        Output: Zellinhalt der ausgewählten Zelle. Datentyp entspricht Datentyp in Zelle.
        """
        try:
            myws = self._blattName
            myCell = myws[self._zelle]
            myCellValue = myCell.value
            print(type(myCellValue))
            return myCellValue
        except FileNotFoundError:
            print("Keine Excel-Datei im gesetzten Ordner vorhanden.\nFehler entsteht in _ladeDatei.\nWird in _zelleAuslesen abgefangen.\n")

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



# # TEST 

initBlattObj = ExcelTable(excelDatei,excelBlatt)
blattKopfdaten = initBlattObj._ladeBlatt()

# initCellObj = CellValueFromExcel(blattKopfdaten,excelZelle1)
# datum1 = initCellObj._einzelneZelleAuslesen()

dict1 = initBlattObj._dictKopfdatenCells
dict2 = initBlattObj._dictKopfdatenValues

for keyval, val in dict1.items():
    inhaltAusZelle = blattKopfdaten[val].value
    dict2[keyval] = inhaltAusZelle

print(dict2["datumVon"])
print(dict2["datumBis"])

# for k, v in dict2.items():
#     print(k,v)

# def _alleKopfdatenZellenAuslesen(self):
#     myws = self._ladeBlatt()
#     myCell = myws[self._zelle]
#     for keyval, val in self._dictKopfdatenCells.items():
#         myCellValue = myCell.value
#         self._dictKopfdatenValues[keyval] = myCellValue
#     return self._dictKopfdatenValues


# zelleInWb = CellValueFromExcel(excelDatei,excelBlatt,excelZelle1)
# ausgelesenerZellWert1 = zelleInWb._einzelneZelleAuslesen()

# zelleInWb = CellValueFromExcel(excelDatei,excelBlatt,excelZelle2)
# ausgelesenerZellWert2 = zelleInWb._einzelneZelleAuslesen()

# print(ausgelesenerZellWert1)
# print(ausgelesenerZellWert2)

# boolTestObj = CompareCellValues(ausgelesenerZellWert1,ausgelesenerZellWert2)
# test = boolTestObj._compare()
# print(test)
                