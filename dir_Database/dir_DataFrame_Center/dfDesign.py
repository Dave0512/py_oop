import pandas as pd


class DfDesigner:
    """
    Class to modify imported file to desired df
    """

    def __init__(self,fileToTransform,sheetName, headerCell):
        """
        docstring
        """
        self._fileToTransform = fileToTransform
        self._sheetName = sheetName
        self._headerCell = headerCell

    def fileToDf(self):
        """
        Input: File, which should be modified to a DataFrame
        Output: DataFrame
        """
        df = pd.read_excel(self._fileToTransform,sheet_name=self._sheetName,dtype=str)
        return df


    def identifyHeaderRow(self):
        """
        Input: Raw Df
        Output: Identified Header Cell as row_start
        """
        df = self.fileToDf()
        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                if df.iat[row,col] == self._headerCell:
                    row_start = row
                    return row_start
                    break
        

    def modifyHeaderDf(self):
        """
        Input: Raw Df, row_start
        Output: DF with new header 
        """
        row_start = self.identifyHeaderRow()
        df = self.fileToDf()
        new_header = df.iloc[row_start] #grab the first row for the header
        df = df[1:] #take the data less the header row
        df.columns = new_header #set the header row as the df header
        df = df.rename(columns = {c: c.replace('*','_MUSS_FELD_') for c in df.columns})
        return df

# TEST

DF = DfDesigner("01_2020_Health Care Sales Report V2.1_Abbott Medical_AGKAMED.xlsm","Bewegungsdaten",'L_Quelle_Name*')
print(DF.modifyHeaderDF().info())