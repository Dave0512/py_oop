

import pandas as pd
import datetime as dt
from lst_fil_in_folder import FileList


class ListToDF:
    """
    Input: Class recieves a list 
    Output: Pandas Dataframe, with the list as a df.series + the inload date
    """

    def __init__(self):
        # self._excludFiles = FileList().excludedFiles() # Recieves List of files which could not be imported
        self._lstTabsError = FileList()._filterTabs()[1]
        self._lstDatError = FileList()._filterDatumsWerte()[1]


    def _extractTables(self):
        """
        Input: List of excluded files
        Output: DF with exluded files and inload date
        """
        lstTabsError = self._lstTabsError
        lstDatError = self._lstDatError
        if lstTabsError:
            seriesExclFiles = pd.Series(lstTabsError)
            dfTabs = pd.DataFrame({'_AusgeschlDateiPfad_': seriesExclFiles
                               ,'_FehlerCode_': "Erforderliche Tabs nicht vorhanden"
                               ,'_date_inload_': str(dt.datetime.now())})

        if lstDatError:
            seriesExclFiles = pd.Series(lstDatError)
            dfDat = pd.DataFrame({'_AusgeschlDateiPfad_': seriesExclFiles
                               ,'_FehlerCode_': "Datum fehlerhaft"
                               ,'_date_inload_': str(dt.datetime.now())})
                
        frames = [dfTabs, dfDat]
        dfErrorFinal = pd.concat(frames)
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

dfCore = ListToDF()
df = dfCore._extractTables()
print(df.info())
print(df.head())