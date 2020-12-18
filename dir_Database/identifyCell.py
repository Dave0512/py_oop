
import pandas as pd

class CellIdentifier:
    """
    Class to find a specific cell e. g. in a Excel Spreetsheet
    """
    def __init__(self,tableAsDF,desiredCellValue):
        self._tableAsDF = tableAsDF
        self._desiredCellValue = desiredCellValue

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
                    if df.iat[row,col] == self._desiredCellValue:
                        row_start = row
                        return row_start
                        break
        
        except Exception as e:
            print(e)
            print("Value not found in first column of table / dataFrame.")

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