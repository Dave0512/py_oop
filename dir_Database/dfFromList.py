

import pandas as pd
import datetime as dt
from lst_fil_in_folder import FileList

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

class ListToDF:
    """
    Input: Class recieves a list 
    Output: Pandas Dataframe, with the list as a df.series + the inload date
    """

    def __init__(self):
        # self._excludFiles = FileList().excludedFiles() # Recieves List of files which could not be imported
        self._lstTabsError = FileList()._filterTabs()[1]
        self._lstDatError = FileList()._filterDatumsWerte()[1]
        self._lstUebError = FileList()._filterUeberschriften()[1]
        self._filterUstIDError = FileList().__filterUstID()[1]
        # ################################################################
        # # Prüfung: UstId - Abgleich mit LieferantenListe UstId in CH Datei
        # # Wenn True: UstId vorhanden = obligatorisch 
        # # Wenn False: FehlerMeldung Lieferant nicht bekannt
        # ################################################################

    def _extractTables(self):
        """
        Input: List of excluded files
        Output: DF with exluded files and inload date
        """
        lstTabsError = self._lstTabsError
        lstDatError = self._lstDatError
        lstUebError = self._lstUebError
        lstUstIdError = self._filterUstIDError
        frames = []

        if lstTabsError:
            seriesExclFiles = pd.Series(lstTabsError)
            dfTabs = pd.DataFrame({'_AusgeschlDateiPfad_': seriesExclFiles
                               ,'_FehlerCode_': "Error: Tabellen"
                               ,'_date_inload_': str(dt.datetime.now())})
            frames.append(dfTabs)

        if lstDatError:
            seriesExclFiles = pd.Series(lstDatError)
            dfDat = pd.DataFrame({'_AusgeschlDateiPfad_': seriesExclFiles
                               ,'_FehlerCode_': "Error: Datum"
                               ,'_date_inload_': str(dt.datetime.now())})
            frames.append(dfDat)

        if lstUebError:
            seriesExclFiles = pd.Series(lstUebError)
            dfUeb = pd.DataFrame({'_AusgeschlDateiPfad_': seriesExclFiles
                            ,'_FehlerCode_': "Error: Ueberschrift"
                            ,'_date_inload_': str(dt.datetime.now())}) 
            frames.append(dfUeb)

        if lstUstIdError:
            seriesExclFiles = pd.Series(lstUstIdError)
            dfUstID = pd.DataFrame({'_AusgeschlDateiPfad_': seriesExclFiles
                            ,'_FehlerCode_': "Error: SenderID (UstID)"
                            ,'_date_inload_': str(dt.datetime.now())}) 
            frames.append(dfUstID)


        print(type(frames))

        try:
            dfErrorFinal = pd.concat(frames)
        except ValueError:
            print("Super, keine Datei fehlerhaft! - None / str wird uebergeben.") # Es wird None übergeben! - Umgang in weiteren Klassen
        else:         
            return dfErrorFinal

        # excludFiles = self._excludFiles 
        # if excludFiles: # Check if faulty files a
        #     seriesExclFiles = pd.Series(excludFiles)
        #     df = pd.DataFrame({'_AusgeschlDateiPfad_': seriesExclFiles
        #                       ,'_date_inload_': str(dt.datetime.now())})
        #     return df
        # else:
        #     print("Jiiieehhhaaa - Keine fehlerhaften Dateien vorhanden.")
    

## TEST

# dfCore = ListToDF()
# df = dfCore._extractTables()
# print(df.info())
# print(df.head())