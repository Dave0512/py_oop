
from typing import ItemsView
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

    def _tabToDf(self):
        try:
            df = pd.DataFrame(self._tableAsDF)
        except:
            print("Df aus Tal erstellen nicht erfolgreich.")
        else:
            return df

    def _locateCellByValue(self):
        """
        Identify Cell by value in dataFrame Col 1. 
        Input: Df
        Output: int
        Ex.: As row_start for header
        """
        try:
            df = self._tabToDf()
            for row in range(df.shape[0]): 
                for col in range(df.shape[1]):
                    if df.iat[row,col] == self._desiredCellValue: # Variabel nach Zellinhalt suchen, um Überschrift zu lokalisieren
                        row_start = row
                        return row_start
                        break
        
        except Exception as e:
            print(e)
            print("Value not found in first column of table / dataFrame.")

    def _tabToDf_WithNewHeader(self):
        """ Set first row as header. Desired for col check in _lstValuesExists """
        try:
            rowToDel = self._locateCellByValue() 
            df = pd.DataFrame(self._tableAsDF) 
            df.columns = df.iloc[rowToDel] # Erste Zeile als Überschriftenzeile setzen
            df.drop(df.index[rowToDel],inplace=True) # Erste Zeile löschen
        except:
            print("Df aus Tbl erstellen nicht erfolgreich.")
        else:
            return df   

    def _lstValuesExists(self):
        """ Check if Überschriften in DF stimmen """
        try:
            if self._locateCellByValue() is not None:
                row_start = self._locateCellByValue()      
                df = self._tabToDf_WithNewHeader()
        except: 
            return None    
        else: 
            if set(df.columns) == set(self._lstBewegungsdatenCols):
                return True
            else:
                return None
        
    def _valueExists(self):
        if self._locateCellByValue() is not None:
            return True
        else:
            return False
            


# #####################
# TEST
# #####################

# pdTest = pd.read_excel("01_2020_Health Care Sales Report V2.1_Abbott Medical_AGKAMED.xlsm"
#                       ,sheet_name="Bewegungsdaten"
#                       ,dtype=str)

# CellIdentObject = CellIdentifier(pdTest,"L_Quelle_Name*")
# print(CellIdentObject._lstValuesExists())
