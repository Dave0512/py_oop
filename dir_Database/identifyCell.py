
import pandas as pd

class CellIndentifier:
    """
    Class to find a specific cell e. g. in a Excel Spreetsheet
    """
    def __init__(self,tableAsDF,desiredCellValue):
        self._tableAsDF = tableAsDF
        self._desiredCellValue = desiredCellValue

    def _locateCellByValue(self):
        """
        Identify Cell by value in dataFrame
        Input: Df
        Output: int
        Ex.: As row_start for header
        """
        df = pd.DataFrame(self._tableAsDF)

        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                if df.iat[row,col] == self._desiredCellValue:
                    row_start = row
                    return row_start
                    break


    # def _identifyHeaderRow(self):
        # """
        # Input: Raw Df
        # Output: Identified Header Cell as row_start
        # """
        # df = self._fileToDf()
        # for row in range(df.shape[0]):
            # for col in range(df.shape[1]):
                # if df.iat[row,col] == self._headerCell:
                    # row_start = row
                    # return row_start
                    # # return df.shape[1]
                    # break


# #####################
# TEST
# #####################

# pdTest = pd.read_excel("Z:\\1_AGKAMED_Arbeit\\0_GIT_REPOS\py_oop\\dir_Database\\dir_Module_File_Handling\\HCSR_Daten_TEST\\02_2020_Health Care Sales Report V2.1_Abbott Medical_AGKAMED.xlsm",sheet_name="Bewegungsdaten",dtype=str) # header=1,
# # pdTest.info()

# CellIdentObject = CellIndentifier(pdTest,"L_Quelle_Name*")#._locateCellByValue()
# # print(type(CellIdentObject._desiredCellValue))
# # print(CellIdentObject._desiredCellValue)

# # print(type(CellIdentObject._tableAsDF))
# # print(CellIdentObject._tableAsDF.info())

# Zelle = CellIdentObject._locateCellByValue()
# print(type(Zelle))
# print(Zelle)
