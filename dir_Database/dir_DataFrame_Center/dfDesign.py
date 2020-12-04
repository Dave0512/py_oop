from typing import final
import numpy
import pandas as pd
import datetime as dt
import numpy as np

from pandas.core.arrays.integer import Int64Dtype
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)



class DfDesigner:
    """
    Class to modify imported file to desired df
    """

    def __init__(self,fileToTransform,sheetName, headerCell):
        """
        Input:  Class Attributes
                Mandatory Informations to create an instance
        """
        self._fileToTransform = fileToTransform
        self._sheetName = sheetName
        self._headerCell = headerCell
        self._lstColToClean = ["L_Quelle_ID_MUSS_FELD_","L_Quelle_Name_MUSS_FELD_","L_Art_ID_MUSS_FELD_","H_Quelle_ID","H_Art_Nr_MUSS_FELD_","H_Art_ID_MUSS_FELD_"]
        # self._lstColToInt = ["Umsatz_MUSS_FELD_"] #,"Steuersatz_MUSS_FELD_","L_VPE_Menge_MUSS_FELD_","BASISME_Auswahl_MUSS_FELD_","Faktor_BASISME_VPE_MUSS_FELD_"]
        self._lstColToInt = ["L_VPE_Menge_MUSS_FELD_","Umsatz_MUSS_FELD_"]

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
        for col in self._lstColToClean:
            df[self._addSuffixToColName(col).name] = self._addSuffixToColName(col) 
        for colInt in self._lstColToInt:
            df[colInt] = df[colInt].astype('float')
        return df 

    def _extractTables(self):
        """
        Create different df extracts to gain other sql tables 
        Input: modified df
        
        Output: extracted dfs
        Ex.: 
            - Pivot-tables, 
            - Extracted content of the df 
              df[["H_Art_Nr_MUSS_FELD_","H_Art_Nr_MUSS_FELD__NORMALIZED"]]

        """ 
        df = self._addColumns()
        dfPiv = pd.pivot_table(df,values=["L_VPE_Menge_MUSS_FELD_","Umsatz_MUSS_FELD_"],index=["L_Quelle_Name_MUSS_FELD_"
                                                                                               ,"L_Quelle_ID_MUSS_FELD_"
                                                                                            #    ,"L_Art_Nr_MUSS_FELD_"
                                                                                               ,"Einrichtung_MUSS_FELD_"], aggfunc=np.sum).reset_index()
  
        return dfPiv      
                    
                    
        

    def createFinalDf(self):
        """
        Main def to execute. Def to be called by an outside client
        Output: Modified df
        """
        finalDf = self._addColumns()
        return finalDf

        
        
# TEST

# dfCore = DfDesigner("01_2020_Health Care Sales Report V2.1_Abbott Medical_AGKAMED.xlsm","Bewegungsdaten",'L_Quelle_Name*')
# # DF = dfCore.createFinalDf()
# DF = dfCore._extractTables()
# print(DF.info())
# print(DF.head())

# print(DF[['L_Art_Nr_MUSS_FELD_','H_Art_Nr_MUSS_FELD_']].head())
# print(dfCore._addSuffixToColName("L_WGRP_Intern"))
