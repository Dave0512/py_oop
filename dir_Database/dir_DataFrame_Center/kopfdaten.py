

import pandas as pd
import openpyxl
from openpyxl import load_workbook
from datetime import datetime

# STRUKTUR
# 1) Dynamisch durch Dateiliste iterieren
# 2) PRÜFUNG: Tabellenblätter vorhanden?
# 3) Tabelle Kopfdaten als ws einladen
# 4) PRÜFUNG: datumVon & datumBis durchführen
# 5) Dict mit Zellinhalten erstellen
# 6) Inhalte mit dateiNamen in DB schreiben

dateiName = "01_2020_Health Care Sales Report V2.1_Abbott Medical_AGKAMED.xlsm"

# ##############
# TESTE openpyxl
# ##############

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

dictKopfdatenValues = {}

# Auslesen der Exceltabelle - erstellen der Variablen
for keyval, val in dictKopfdatenCells.items():
    inhaltAusZelle = ws_openpyxl[val].value
    dictKopfdatenValues[keyval] = inhaltAusZelle


if dictKopfdatenValues['datumBis'] > dictKopfdatenValues['datumVon']:
    print("Prüfung der Datumswerte {0} {1} ist erfolgreich verlaufen.\n\nProzess -Kopfdatenprüfung- kann vorgesetzt werden.".format(dictKopfdatenValues['datumBis'],dictKopfdatenValues['datumVon']))

else:
    print("Daten fehlerhaft. Datei wird mit Fehlercode (Datum) in DB geschrieben.")
  
