import pandas as pd
import datetime as dt
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)



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

    def _fileToDf(self):
        """
        Input: File, which should be modified to a DataFrame
        Output: DataFrame
        """
        df = pd.read_excel(self._fileToTransform,sheet_name=self._sheetName,dtype=str)
        return df


    def _identifyHeaderRow(self):
        """
        Input: Raw Df
        Output: Identified Header Cell as row_start
        """
        df = self._fileToDf()
        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                if df.iat[row,col] == self._headerCell:
                    row_start = row
                    return row_start
                    break
        

    def _modifyHeaderDf(self):
        """
        Input: Raw Df, row_start
        Output: DF with new header 
        """
        row_start = self._identifyHeaderRow()
        df = self._fileToDf()
        new_header = df.iloc[row_start] #grab the first row for the header
        df = df[1:] #take the data less the header row
        df.columns = new_header #set the header row as the df header
        df = df.rename(columns = {c: c.replace('*','_MUSS_FELD_') for c in df.columns})
        return df

    def _clearSpecialCharacters(self,dfSeries):
        """
        Input: DF and dfSeries-Name of the df, which has to be cleaned
        Output: Cleaned Series 

        """
        df = self._modifyHeaderDf()
        dfSeries = df[dfSeries].str.replace(r'\W','') 
        return dfSeries
    
    def _addSuffixToColName(self,dfSeries):
        """
        Input: Recieved cleaned dfSeries-Name
        Output: SeriesName with suffix added
        """
        dfSeries = self._clearSpecialCharacters(dfSeries)
        dfSeries = dfSeries.rename(str(dfSeries.name) + "_NORMALIZED")
        return dfSeries
        
        

    def _addColumns(self):
        """
        Input: DF 
        Output: DF supplemented by columns with and without content
        """
        df = self._modifyHeaderDf()
        
        df['_date_inload_'] = dt.datetime.now()
        df[self._addSuffixToColName("H_Art_Nr_MUSS_FELD_").name] = self._addSuffixToColName("H_Art_Nr_MUSS_FELD_") 
        return df[["H_Art_Nr_MUSS_FELD_","H_Art_Nr_MUSS_FELD__NORMALIZED"]]

        
# TEST

dfCore = DfDesigner("01_2020_Health Care Sales Report V2.1_Abbott Medical_AGKAMED.xlsm","Bewegungsdaten",'L_Quelle_Name*')
DF = dfCore._addColumns()
print(DF.head(100))
# print(DF[['L_Art_Nr_MUSS_FELD_','H_Art_Nr_MUSS_FELD_']].head())
# print(dfCore._addSuffixToColName("L_WGRP_Intern"))
