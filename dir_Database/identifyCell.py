
import pandas as pd

class CellIdentifier:
    """
    Class to find a specific cell e. g. in a Excel Spreetsheet
    """
    def __init__(self,tableAsDF,desiredCellValue):
        self._tableAsDF = tableAsDF
        self._desiredCellValue = desiredCellValue
        self._lstBewegungsdatenCols = ['L_Quelle_Name*'
                                    ,'L_Quelle_IDTyp_Auswahl*'
                                    ,'L_Quelle_ID*'
                                    ,'H_Quelle_Name'
                                    ,'H_Quelle_IDTyp_Auswahl'
                                    ,'H_Quelle_ID'
                                    ,'Einrichtung*'
                                    ,'Organisation_ID_Auswahl*'
                                    ,'Organisation_ID*'
                                    ,'L_Art_Nr*'
                                    ,'L_Art_IDTyp_Auswahl'
                                    ,'L_Art_ID*'
                                    ,'H_Art_Nr*'
                                    ,'H_Art_IDTyp_Auswahl'
                                    ,'H_Art_ID*'
                                    ,'L_Art_Txt*'
                                    ,'L_WGRP_Intern'
                                    ,'L_WGRP_Merkmale_Intern'
                                    ,'L_VPE_Auswahl*'
                                    ,'L_VPE_Menge*'
                                    ,'Faktor_BASISME_VPE*'
                                    ,'BASISME_Auswahl*'
                                    ,'Steuersatz Landescode*'
                                    ,'Steuersatz*'
                                    ,'Umsatz*'
                                    ,'Bonusrelevant*']

    def _locateCellByValue(self):
        """
        Identify Cell by value in dataFrame Col 1. 
        Input: Df
        Output: int
        Ex.: As row_start for header
        """
        try:
            df = pd.DataFrame(self._tableAsDF)

            for row in range(df.shape[0]): 
                for col in range(df.shape[1]):
                    if df.iat[row,col] == self._desiredCellValue: # Variabel nach Zellinhalt suchen, um Überschrift zu lokalisieren
                        row_start = row
                        return row_start
                        break
        
        except Exception as e:
            print(e)
            print("Value not found in first column of table / dataFrame.")

    def _lstValuesExists(self):
        try:
            row_start = self._locateCellByValue()
            _headerRow = row_start
            df = pd.DataFrame(self._tableAsDF,header=_headerRow)
        except:
            return None
        else: 
            if all([item in df.columns for item in self._lstBewegungsdatenCols]) is not None:
                return True
            else:
                return False
        

    def _valueExists(self):
        if self._locateCellByValue() is not None:
            return True
        else:
            return False
            
        

# #####################
# TEST
# #####################

# pdTest = pd.read_excel("Z:\\1_AGKAMED_Arbeit\\0_GIT_REPOS\py_oop\\dir_Database\\dir_Module_File_Handling\\HCSR_Daten_TEST\\02_2020_Health Care Sales Report V2.1_Abbott Medical_AGKAMED.xlsm",sheet_name="Bewegungsdaten",dtype=str) # header=1,
# pdTest.info()

# CellIdentObject = CellIdentifier(pdTest,"L_Quelle_Name*")#._locateCellByValue()
# # print(type(CellIdentObject._desiredCellValue))
# # print(CellIdentObject._desiredCellValue)

# # print(type(CellIdentObject._tableAsDF))
# # print(CellIdentObject._tableAsDF.info())

# # Zelle = CellIdentObject._locateCellByValue()
# # print(type(Zelle))
# # print(Zelle)

# WahrFalsch = CellIdentObject._valueExists()
# print(WahrFalsch)