
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

    def _lstValuesExists(self):
        # try:
        if self._locateCellByValue() is not None:
            row_start = self._locateCellByValue()   
            print(row_start)    
        else: 
            print("Überschrift nicht vorhanden")          
        # _headerRow = row_start
        # df = pd.read_excel(self._tableAsDF,header=_headerRow)
        # print(df.columns)
        # # [i for i, j in zip(a, b) if i == j] # Gibt die Daten aus die übereinstimmen
        # # except:
        # #     return None
        # # else: 
        # #     print(df.columns)
        # #     # if all([item in df.columns for item in self._lstBewegungsdatenCols]) is not None:
        # #     #     return True
        # #     # else:
        # #     #     return None
        

    def _valueExists(self):
        if self._locateCellByValue() is not None:
            return True
        else:
            return False
            


# #####################
# TEST
# #####################

pdTest = pd.read_excel("01_2020_Health Care Sales Report V2.1_Abbott Medical_AGKAMED.xlsm"
                      ,sheet_name="Bewegungsdaten"
                      ,dtype=str) #,header=1)

# # print(pdTest.columns)

CellIdentObject = CellIdentifier(pdTest,"L_Quelle_Name*")
print(CellIdentObject._locateCellByValue())
# # ueberschriften = CellIdentObject._lstBewegungsdatenCols
# # [print(c) for c in ueberschriften]


print(CellIdentObject._lstValuesExists())
# print(CellIdentObject._valueExists())

# # print(type(CellIdentObject._tableAsDF))
# # print(CellIdentObject._tableAsDF.info())

# Zelle = CellIdentObject._locateCellByValue()
# print(type(Zelle))
# print(Zelle)

# WahrFalsch = CellIdentObject._valueExists()
# print(WahrFalsch)

