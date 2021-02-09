

import pandas as pd

import xlrd
from datetime import datetime
dateiName = "01_2020_Health Care Sales Report V2.1_Abbott Medical_AGKAMED.xlsm"

# ##############
# TESTE openpyxl
# ##############
import openpyxl
from openpyxl import load_workbook
wb_openpyxl = openpyxl.load_workbook(dateiName)
ws_openpyxl = wb_openpyxl['Kopfdaten']
# print(type(wb_openpyxl))
# [print(type(ws)) for ws in wb_openpyxl.sheetnames if ws == "Kopfdaten"]

# ###################
# Kopfdaten Variablen
# ###################

dictKopfdatenCells = {"datumVon":"E8"
                  ,"datumBis":"E10"
                  ,"senderName":"E32"
                  ,"senderIdAuswahl":"E34"
                  ,"senderId":"E36"}

# Auslesen der Exceltabelle - erstellen der Variablen
for keyval, val in dictKopfdatenCells.items():
    inhaltAusZelle = ws_openpyxl[val].value
    dictKopfdatenValues = {keyval:inhaltAusZelle}
    # print(dictKopfdatenValues)
 
    

# datumVon = ws_openpyxl['E8'].value
# datumBis = ws_openpyxl['E10'].value
# senderName = ws_openpyxl['E32'].value
# senderIdAuswahl = ws_openpyxl['E34'].value
# senderId =  ws_openpyxl['E36'].value

# if datumBis > datumVon:
#     print("Prüfung der Datumswerte {0} {1} ist erfolgreich verlaufen.\n\nProzess -Kopfdatenprüfung- kann vorgesetzt werden.".format(datumVon,datumBis))
# else:
#     print("Daten fehlerhaft. Datei wird mit Fehlercode (Datum) in DB geschrieben.")
  

# ws_openpyxl = wb_openpyxl.get_sheet_by_name('Sheet1')

# valueConv =  datetime.strptime(value, '%y/%m/%d')
# cell_value = worksheet.cell(8, 4).value

# # print(MeldedatumBis)
# print(test)
# datum = datetime.fromtimestamp(MeldedatumVon).strftime('%Y-%m-%d')
# datumBis = datetime.fromtimestamp(MeldedatumBis).strftime('%Y-%m-%d')
# # print(datum)
# print(datumBis)

# from pyxlsb import convert_date
# convert_date(MeldedatumBis)
# format(convert_date(MeldedatumBis), '%m/%d/%Y')
# print(MeldedatumBis)


# ##########################
# TEST PANDAS to HANDLE xlsx
# ##########################
# df = pd.read_excel(dateiName,sheet_name=None)

# for v in df:
#     if v != "Bewegungsdaten":
#         print(v)