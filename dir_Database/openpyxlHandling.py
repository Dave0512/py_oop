
from openpyxl.descriptors.base import Bool
import pandas as pd
import openpyxl
from openpyxl import load_workbook
from datetime import datetime

excelDatei = "dir_DataFrame_Center\\01_2020_Health Care Sales Report V2.1_Abbott Medical_AGKAMED.xlsm"

excelBlatt = "Kopfdaten"

excelZelle = "E8"


class CellValueFromExcel:
    """
    Class to extract Cell Values from an excelfile, excelsheet
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
    def __init__(self,value1,value2):
        self._value1 = value1
        self._value2 = value2
    
    def _compare(self):
        if self._value1 == self._value2:
            return True
        else:
            return False

# TEST 

# boolTestObj = CompareCellValues(2,"2")
# test = boolTestObj._compare()
# print(test)
        
# TEST

# wb = CellValueFromExcel(excelDatei,excelBlatt,excelZelle)
# ausgelesenerZellWert = wb._zelleAuslesen()
# print(ausgelesenerZellWert)

        


        