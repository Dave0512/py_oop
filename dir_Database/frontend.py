

import sys
from typing import Type 
import pandas as pd

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QListWidget, QLineEdit, QTextEdit,QMessageBox,QTableWidget,QTableWidgetItem, QHeaderView
from PyQt5.QtGui import *

import main
from main import ausfuehren, dfFromSQLHcsrFilesImported #, pandasModel

from PyQt5.QtWidgets import QTableView, QProgressBar, QLabel
from PyQt5.QtCore import QAbstractTableModel, QSortFilterProxyModel, Qt

# ####################
# Import eigene Klasse
# ####################
# import py_etl_sql_funktionen
# from ipynb.fs.full.py_etl_sql_funktionen import sql_ausfuehrung
import ipynb
import import_ipynb
import py_migriere_zip_handling_Entwicklung
from ipynb.fs.full.py_migriere_zip_handling_Entwicklung import handling_export_warenkorb, handling_export_warenkorb_gtin


class Fenster(QWidget):

    def __init__(self):
        super().__init__()
        self.initMe()

    def _loadDataFromDB(self):
        """
        Displays DB Informations in GUI Table
        Input: List of Dicts of DB result of SQL Query
        Output: Values in QTableWidget 
        """
        try:
            result = dfFromSQLHcsrFilesImported()
        except:         
            QMessageBox.information(self,"HCSR-Importer",
                                    "Tabelle 'HCSR' existiert noch nicht."                                
                                    "\nBitte zunächst Daten importieren, damit"
                                    "\nInfos angezeigt werden können.")
        else:
            rngDictsInList = range(len(result)) # Dicts are DB values with headers
            # self.lstbox_hcsr.setRowCount(0)
            while self.lstbox_hcsr.rowCount() > 0:
                self.lstbox_hcsr.removeRow(0)
            self.lstbox_hcsr.setSortingEnabled(False)
            header_labels = ["Lieferant", "Dateiname", "Anzahl Artikel", "Einladedatum"]
            self.lstbox_hcsr.setColumnCount(len(header_labels)) 
            self.lstbox_hcsr.setHorizontalHeaderLabels(header_labels)
            # self.lstbox_hcsr.horizontalHeader().setSectionResizeMode(0,QHeaderView.ResizeToContents)            
            for d in result:
                for x in rngDictsInList:
                    x-=len(result)-1 # Dynamisch: Die Anzahl der zu "löschenden" Zeilen, damit die Zeilen ohne Leerzeilen angezeigt werden
                    self.lstbox_hcsr.insertRow(x)                
                for column_number, data in enumerate(d.values()):
                    self.lstbox_hcsr.setItem(x,column_number,QtWidgets.QTableWidgetItem(str(data)))

            self.lstbox_hcsr.resizeColumnsToContents()
            self.lstbox_hcsr.resizeRowsToContents()
            self.lstbox_hcsr.setSortingEnabled(True)
 
    def initMe(self):
        self.label = QLabel("Dashboard")
        self.label.setGeometry(200,25,500,25)

        self.lstbox_hcsr=QTableWidget(self)
        self.lstbox_hcsr.setGeometry(50,150,1500,700) 
        self.lstbox_hcsr.setSortingEnabled(True)
        header_labels = ["Lieferant", "Dateiname", "Anzahl Artikel", "Einladedatum"]
        self.lstbox_hcsr.setColumnCount(len(header_labels)) 
        self.lstbox_hcsr.setHorizontalHeaderLabels(header_labels)
        # self.lstbox_hcsr.horizontalHeader().setSectionResizeMode(0,QHeaderView.ResizeToContents)

        self.progress = QProgressBar(self)
        self.progress.setGeometry(50,25,950,25)  

        self.btn_show_hcsr_in_tbl=QPushButton("Zeige HCSR",self) 
        self.btn_show_hcsr_in_tbl.setGeometry(650,70,200,25)   
        self.btn_show_hcsr_in_tbl.clicked.connect(self._loadDataFromDB)

        self.btn_import=QPushButton("HCSR Import starten",self) 
        self.btn_import.move(50,110)
        self.btn_import.setGeometry(50,70,200,25) 
        self.btn_import.clicked.connect(self._download)
        self.btn_import.clicked.connect(self._importHCSR)   
        self.btn_import.clicked.connect(self._download)     
        self.btn_import.clicked.connect(self._call_msg)


        self.btn_import=QPushButton("HCSR Export starten",self) 
        self.btn_import.setGeometry(350,70,200,25) 

        # self.btn_Katalog_import=QPushButton("Katalog Import starten",self) 
        # self.btn_Katalog_import.setGeometry(650,70,200,25)   
        
        self.setGeometry(50,50, 2000, 1000)
        self.setWindowTitle("Katalogmanagement / HCSR Import") 
        self.setWindowIcon(QIcon("agkamed.jpg")) 

        self.btn_exit=QPushButton("Tool schließen",self) 
        self.btn_exit.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.btn_exit.setGeometry(50,900,200,25)

        self.txt_suche=QLineEdit(self) 
        self.txt_suche.setGeometry(50,100,900,25)
        self.txt_suche.setStyleSheet('font-size: 35 px; height: 60px')

        self.btn_map_warenkorb=QPushButton("Katalog Mapping starten (ecl@ss)",self)
        self.btn_map_warenkorb.setGeometry(1650,100,200,25) 
        self.btn_map_warenkorb.setToolTip("Warenkorb für IT-Projekt in Importordner ablegen."
                                          "Mapping erfolgt via Key Lieferant_ArtikelNr\n"
                                          "Stelle daher bitte sicher, dass Lieferant_ArtikelNr\n"
                                          "im Warenkorb eingetragen sind.")
        self.btn_map_warenkorb.clicked.connect(py_migriere_zip_handling_Entwicklung.handling_export_warenkorb) # ETL Warenkorbmapping DEF anbinden
        self.btn_map_warenkorb.clicked.connect(self._call_msg_katalog_map)

        self.btn_map_warenkorb_gtin=QPushButton("Katalog Mapping starten (GTIN)",self)
        self.btn_map_warenkorb_gtin.setGeometry(1650,70,200,25) 
        self.btn_map_warenkorb_gtin.setToolTip("Warenkorb für IT-Projekt in Importordner ablegen.\n"
                                          "Mapping erfolgt via Key Lieferant_ArtikelNr_NOU_UOM.\n"
                                          "Stelle daher bitte sicher, dass NOU & UOM im EDIFACT-Format\n"
                                          "im Warenkorb eingetragen sind.")
        self.btn_map_warenkorb_gtin.clicked.connect(py_migriere_zip_handling_Entwicklung.handling_export_warenkorb_gtin) # ETL Warenkorbmapping DEF anbinden
        self.btn_map_warenkorb_gtin.clicked.connect(self._call_msg_katalog_map)
        # ################
        self.btn_import_lief=QPushButton("Lieferantenliste (CH) Import",self)
        self.btn_import_lief.setGeometry(1650,300,200,25) 

        self.showMaximized()

    def _importHCSR(self):
        main.ausfuehren()

    def _call_msg(self):
        QMessageBox.information(self,"HCSR-Importer",
                                "\nImport wurde erfolgreich durchgeführt.")

    def _call_msg_katalog_map(self):
        QMessageBox.information(self,"Katalog-Mapping",
                                "\nWarenkorb wurde erfolgreich gemappt.\n"
                                "Das Resultat liegt im Exportordner ... bereit.")


    def _suche(self,value):
        value = self.txt_suche.text()

        if value == 0:
            QMessageBox.information(self,"Warning","Search query can not be empty!")
        else:
            self.txt_suche.setText("")

    def _download(self):
        self.completed = 0
        while self.completed < 100:
            self.completed += 0.0001
            # self.completed += 0.00001
            self.progress.setValue(self.completed) # Set Value of ProgressBar       

style = '''

QWidget {
    background-color: #fcfdff;
} 

QLabel {
    font: medium Ubuntu;
    font-size: 20px;
    color: #006325;     
}        

QPushButton {
    background-color: #edeef0;
    color: black;

}
QPushButton:hover {
    background-color: #808080;
}
QPushButton:pressed {
    background-color: #80c342;
}    

'''

        
if __name__ == "__main__":

    
    
        
    app=QApplication(sys.argv) 
    app.setStyleSheet(style)
    w=Fenster()
    # p = w.palette() 
    # # p.setColor(w.backgroundRole(), Qt.lightGray) # Hintergrundfarbe
    # # w.setStyleSheet("color: rgb(255, 0, 0);") # Schriftfarbe
    
    # w.setPalette(p) 
    sys.exit(app.exec_())
  





