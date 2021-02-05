

import sys
from typing import Type 
import pandas as pd

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QListWidget, QLineEdit, QTextEdit,QMessageBox,QTableWidget,QTableWidgetItem, QHeaderView
from PyQt5.QtGui import *

import main
from main import ausfuehren, dfFromSQLHcsrFilesImported #, pandasModel

from PyQt5.QtWidgets import QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt

df = dfFromSQLHcsrFilesImported() # Ergebnis aus DB Query 
from pandasToTable import TableView # HIER
data = {'col1':['1','2','3','4'],
        'col2':['1','2','1','3'],
        'col3':['1','1','2','1']}

# table = TableView(data,10,10)

# def main(args):
#     app = QApplication(args)
#     table = TableView(data,10,10)
#     table.show()
#     sys.exit(app.exec_())

# if __name__ == "__main__":
#     main(sys.argv)
    
# class pandasModel(QAbstractTableModel):
    
#     def __init__(self, data):
#         QAbstractTableModel.__init__(self)
#         self._data = data

#     def rowCount(self, parent=None):
#         return self._data.shape[0]

#     def columnCount(self, parnet=None):
#         return self._data.shape[1]

#     def data(self, index, role=Qt.DisplayRole):
#         if index.isValid():
#             if role == Qt.DisplayRole:
#                 return str(self._data.iloc[index.row(), index.column()])
#         return None

#     def headerData(self, col, orientation, role):
#         if orientation == Qt.Horizontal and role == Qt.DisplayRole:
#             return self._data.columns[col]
#         return None



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
        result = dfFromSQLHcsrFilesImported()
        anzahlDictsInList = range(len(result)) # Dicts are DB values with headers
        self.lstbox_hcsr.setRowCount(0)
         
        for d in result:
            for x in anzahlDictsInList:
                x-=1
                self.lstbox_hcsr.insertRow(x)  
            for column_number, data in enumerate(d.values()):
                self.lstbox_hcsr.setItem(x,column_number,QtWidgets.QTableWidgetItem(str(data)))
        
    def initMe(self):
        self.lstbox_hcsr=QTableWidget(self)
        self.lstbox_hcsr.setColumnCount(4) 
        self.lstbox_hcsr.setGeometry(50,150,700,700) 

        self.btn_show_hcsr_in_tbl=QPushButton("Zeige HCSR",self) 
        self.btn_show_hcsr_in_tbl.setGeometry(650,70,200,25)   
        self.btn_show_hcsr_in_tbl.clicked.connect(self._loadDataFromDB)

        self.btn_import=QPushButton("HCSR Import starten",self) 
        self.btn_import.move(50,110)
        self.btn_import.setGeometry(50,70,200,25) 

        self.btn_import.clicked.connect(self._importHCSR)
        self.btn_import.clicked.connect(self._call_msg)

        self.btn_import=QPushButton("HCSR Export starten",self) 
        self.btn_import.setGeometry(350,70,200,25) 

        # self.btn_Katalog_import=QPushButton("Katalog Import starten",self) 
        # self.btn_Katalog_import.setGeometry(650,70,200,25)   
        
        self.setGeometry(50,50, 2000, 1000)
        self.setWindowTitle("Katalogmanagement / HCSR Import") 
        self.setWindowIcon(QIcon("agkamed.jpg")) 

        self.btn_exit=QPushButton("Tool schließen",self) 
        # self.btn_exit.move(50,1000) 
        self.btn_exit.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.btn_exit.setGeometry(50,900,200,25)

        self.txt_suche=QLineEdit(self) 
        self.txt_suche.setGeometry(50,100,900,25)





        self.btn_map_warenkorb=QPushButton("Katalog Mapping starten",self)
        self.btn_map_warenkorb.setGeometry(950,70,200,25) 
        self.btn_map_warenkorb.setToolTip("Warenkorb für IT-Projekt in Importordner ablegen.")
        # self.btn_map_warenkorb.clicked.connect() # ETL Warenkorbmapping DEF anbinden

        # self.lstbox_hcsr.setHorizontalHeaderItem(0,QTableWidgetItem("Lieferant"))
        # self.lstbox_hcsr.horizontalHeader().setSectionResizeMode(0,QHeaderView.ResizeToContents)

        # self.lstbox_hcsr.setHorizontalHeaderItem(1,QTableWidgetItem("Dateiname"))
        # self.lstbox_hcsr.horizontalHeader().setSectionResizeMode(1,QHeaderView.ResizeToContents)

        # self.lstbox_hcsr.setHorizontalHeaderItem(2,QTableWidgetItem("Anzahl Artikel"))
        # self.lstbox_hcsr.horizontalHeader().setSectionResizeMode(2,QHeaderView.ResizeToContents)

        # self.lstbox_hcsr.setHorizontalHeaderItem(3,QTableWidgetItem("Einrichtung"))
        # self.lstbox_hcsr.horizontalHeader().setSectionResizeMode(3,QHeaderView.ResizeToContents)

        # self.lstbox_hcsr.setHorizontalHeaderItem(4,QTableWidgetItem("Umsatz"))
        # self.lstbox_hcsr.horizontalHeader().setSectionResizeMode(4,QHeaderView.ResizeToContents)

        self.show()

    def _importHCSR(self):
        main.ausfuehren()

    def _call_msg(self):
        QMessageBox.information(self,"HSCR",
                                "\nImport wurde erfolgreich durchgeführt.")


        
if __name__ == "__main__":
    app=QApplication(sys.argv) 
    w=Fenster() 
    sys.exit(app.exec_())
  

    # print(df)




