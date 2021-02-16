from typing import final
import numpy
import pandas as pd
import datetime as dt
import numpy as np
import sys

from pandas.tseries.offsets import Day
from lst_fil_in_folder import FileList
from identifyCell import CellIdentifier


# from pandas.core.arrays.integer import Int64Dtype
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


class DFBase: # Basis Struktur
    """
    Base Class for DF Design
    """
    def __init__(self): # Vorbelegte Basis-Attribute
        pass
    
    # 1
    def _fileToDf(self): # .xls, .csv, .xml
        pass

    # 2
    def _identifyHeaderRow(self):
        pass

    # 3
    def _modifyHeaderDf(self):
        pass

    # 4
    def _clearSpecialCharacters(self,dfSeries):
        pass
    
    # 5
    def _addSuffixToColName(self,dfSeries):
        pass
    
    # 6 
    def _addColumns(self):
        pass

    # 7
    def _extractTables(self):
        raise NotImplementedError()
        pass

    # 8
    def _createFinalDf(self):
        pass
    


class TableToDF: # Basis
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
        self._lstColToInt =   ["L_VPE_Menge_MUSS_FELD_"
                              ,"Umsatz_MUSS_FELD_"]
        self._pivValCols =    ["L_VPE_Menge_MUSS_FELD_"
                              ,"Umsatz_MUSS_FELD_"]
        self._pivIndexCols =  ["L_Quelle_Name_MUSS_FELD_"
                              ,"L_Quelle_ID_MUSS_FELD_"
                              ,"Einrichtung_MUSS_FELD_"                              
                              ,"L_Art_Nr_MUSS_FELD_"
                              ,"L_Art_Txt_MUSS_FELD_"]
        

    def _fileToDf(self):
        """
        Input: File, which should be modified to a DataFrame
        Output: DataFrame
        """
        try:
            if self._fileToTransform[-1] == "b":          
                df = pd.read_excel(self._fileToTransform,sheet_name=self._sheetName,dtype=str, engine='pyxlsb')
            else:
                df = pd.read_excel(self._fileToTransform,sheet_name=self._sheetName,dtype=str)
            return df
        except Exception as e:
            print(e)

    def _modifyHeaderDf(self):
        """
        Input: Raw Df, row_start
        Output: DF with new header 
        """
        
        df = self._fileToDf()
        row_start = CellIdentifier(df,self._headerCell)._locateCellByValue()
        # if row_start is not None:           
        new_header = df.iloc[row_start] #grab the first row for the header
        df = df[row_start+1:] #take the data less the header row
        df.columns = new_header #set the header row as the df header
        df = df.rename(columns = {c: c.replace('*','_MUSS_FELD_') for c in df.columns})
        return df
        # else: 
            # print("Überschrift nicht vorhanden. Bei File {0} lautet RowStart: {1}".format(df.head(1),row_start))
            # pass
            

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
        df['_DateiName_'] = self._fileToTransform.split("\\")[-1]
        df['_DateiNameCompKey_'] = df['_DateiName_'].astype(str) + "°" + df['_date_inload_'].astype(str)
        for col in self._lstColToClean:
            df[self._addSuffixToColName(col).name] = self._addSuffixToColName(col) 
        for colInt in self._lstColToInt:
            df[colInt] = df[colInt].astype('float')
        return df 

    def _nameRelCols(self):
        """
        Input: _addColumns DF
        Output: DF with selected columns
        """
        
        df = self._addColumns()
        df = df[["L_Quelle_Name_MUSS_FELD_",
                "L_Quelle_IDTyp_Auswahl_MUSS_FELD_",
                "L_Quelle_ID_MUSS_FELD_",
                "H_Quelle_Name",
                "H_Quelle_IDTyp_Auswahl",
                "H_Quelle_ID",
                "Einrichtung_MUSS_FELD_",
                "Organisation_ID_Auswahl_MUSS_FELD_",
                "Organisation_ID_MUSS_FELD_",
                "L_Art_Nr_MUSS_FELD_",
                "L_Art_IDTyp_Auswahl",
                "L_Art_ID_MUSS_FELD_",
                "H_Art_Nr_MUSS_FELD_",
                "H_Art_IDTyp_Auswahl",
                "H_Art_ID_MUSS_FELD_",
                "L_Art_Txt_MUSS_FELD_",
                "L_WGRP_Intern",
                "L_WGRP_Merkmale_Intern",
                "L_VPE_Auswahl_MUSS_FELD_",
                "L_VPE_Menge_MUSS_FELD_",
                "Faktor_BASISME_VPE_MUSS_FELD_",
                "BASISME_Auswahl_MUSS_FELD_",
                "Steuersatz Landescode_MUSS_FELD_",
                "Steuersatz_MUSS_FELD_",
                "Umsatz_MUSS_FELD_",
                "Bonusrelevant_MUSS_FELD_",
                "_date_inload_",
                "_DateiName_",
                "L_Quelle_ID_MUSS_FELD__NORMALIZED",
                "L_Quelle_Name_MUSS_FELD__NORMALIZED",
                "L_Art_ID_MUSS_FELD__NORMALIZED",
                "H_Quelle_ID_NORMALIZED",
                "H_Art_Nr_MUSS_FELD__NORMALIZED",
                "H_Art_ID_MUSS_FELD__NORMALIZED"]]
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
        raise NotImplementedError() 
                    
    def _createFinalDf(self):
        """
        Main def to execute. Def to be called by an outside client
        Output: Modified df
        """
        finalDf = self._nameRelCols()
        return finalDf


    # def _KopfdatenAuslesen(self):
        # """
        # Kopfdaten 
        # """
        
    # def doProgress(self):
        # """
        # Do Progress Def if sheetName = "Bewegungsdaten"
        # """

        # try:
        #   if self._sheetName == "Bewegungsdaten":
            #   self._createFinalDf()
        #   else: # Kopfdaten
            #   self._KopfdatenAuslesen()
        # except Exception as e:
            # print(e)

# ###########
# Inheritance
# ###########

class DfDesignerPiv(TableToDF):
    """
    Inheritance of Base Class DfDesigner
    Recieves all Base-Class Attributes with default values
    """
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
        df = self._nameRelCols()
        dfPiv = pd.pivot_table(df,values=self._pivValCols,index=self._pivIndexCols, aggfunc=np.sum).reset_index()  
        return dfPiv  


# dfCore = TableToDF("dir_DataFrame_Center\\HCSR_Daten_kurz\\05_2020_Health Care Sales Report V2.1_Abbott Medical_AGKAMED.xlsm", "Bewegungsdaten", "L_Quelle_Name*")

# col = dfCore._identifyHeaderRow()

# print(col)
# print(df.info())

















# ###############################################

# #################
# TEST Basis Klasse
# #################


# dfCore = DfDesigner("01_2020_Health Care Sales Report V2.1_Abbott Medical_AGKAMED.xlsm","Bewegungsdaten",'L_Quelle_Name*')
# DF = dfCore._createFinalDf()
# print(DF.info())
# print(DF.head())

# ###################
# TEST Geerbte Klasse
# ###################

# dfCoreErbe = DfDesignerPiv("01_2020_Health Care Sales Report V2.1_Abbott Medical_AGKAMED.xlsm","Bewegungsdaten",'L_Quelle_Name*')
# DFErbe = dfCoreErbe._extractTables()
# print(DFErbe.info())
# print(DFErbe.head())



# Lister = FileList()
# lstHCSR = Lister.filterFileList()
# for hcsrFile in lstHCSR:
    # print(hcsrFile)


    # dfExcl = DfExclFiles(fileToTransform=hcsrFile,sheetName=Lister._kriteriumIdentifikationDatei,headerCell='L_Quelle_Name*')
    # df = dfExcl._extractTables()
    # print(df.info())