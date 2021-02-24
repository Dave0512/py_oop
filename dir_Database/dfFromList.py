

import pandas as pd
import datetime as dt
from lst_fil_in_folder import FileList


class ListToDF:
    """
    Input: Class recieves a list 
    Output: Pandas Dataframe, with the list as a df.series + the inload date
    """

    def __init__(self):
        self._excludFiles = FileList().excludedFiles() # Recieves List of files which could not be imported
        self._lstTabsError = FileList()._filterTabs()[1]


    def _extractTables(self):
        """
        Input: List of excluded files
        Output: DF with exluded files and inload date
        """
        lstTabsError = self._lstTabsError
        if lstTabsError:
            seriesExclFiles = pd.Series(lstTabsError)
            df = pd.DataFrame({'_AusgeschlDateiPfad_': seriesExclFiles
                               ,'_FehlerCode_': "Erforderliche Tabs nicht vorhanden"
                               ,'_date_inload_': str(dt.datetime.now())})
            return df
        else:
            print("Jiiieehhhaaa - Keine fehlerhaften Dateien vorhanden.")
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