

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

# Tabellenblatt via openpyxl einladen

wb_openpyxl = openpyxl.load_workbook(dateiName)
ws_openpyxl = wb_openpyxl['Kopfdaten']

# # Class
# Openpyxl Workbook aus Datei erstellen
# Openpyxl aus Sheet in Datei erstellen (Vorbelegen mit "Kopfdaten")
# Variablen für Informationen welche aus Tabelle extrahiert werden müssen
# # Class Method
# Prüfung, ob datumBis > datumVon -> Indikator für valide HCSR Datei
# - TRUE -> in HCSR Tab einladen
# - FALSE -> Mit Fehlercode in Tab hcsrFilesExcluded

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
    # print("Prüfung der Datumswerte {0} {1} ist erfolgreich verlaufen.\n\nProzess -Kopfdatenprüfung- kann vorgesetzt werden.".format(dictKopfdatenValues['datumBis'],dictKopfdatenValues['datumVon']))
    for k, v in dictKopfdatenValues.items():
        print(k)
else:
    print("Daten fehlerhaft. Datei wird mit Fehlercode (Datum) in DB geschrieben.")
  


