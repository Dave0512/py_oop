
import pandas as pd
from lst_fil_in_folder import FileList

FLister = FileList()

# xl = pd.ExcelFile('01_2020_Health Care Sales Report V2.1_Abbott Medical_AGKAMED - Kopie.xlsm')
# ws = xl.sheet_names
# df =  xl.parse('Bewegungsdaten')
# print(df.info())

excelFileListe = FLister.searchFile() # Liste alle ExcelDateien in Ordner Baum

wichtigesBlatt = "Bewegungsdaten" # Name der obligatorischen ExcelBlätter

lstRelevanteExcelFiles = [] # Liste für identifizierte HCSR-Dateien

for file in excelFileListe:
    xl = pd.ExcelFile(file) 
    ws = xl.sheet_names
    for blatt in ws: 
        if str(blatt) == wichtigesBlatt:
            lstRelevanteExcelFiles.append(file)
            # print("Datei: {0} enthält folgende Spalten: {1}".format(file, ws))

print(lstRelevanteExcelFiles)

print("\nAnzahl identifizierte Exceldateien: " + str(len(lstRelevanteExcelFiles)))
