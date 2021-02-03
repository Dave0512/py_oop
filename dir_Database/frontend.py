

import sys 

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QListWidget, QLineEdit, QTextEdit,QMessageBox,QTableWidget,QTableWidgetItem, QHeaderView
from PyQt5.QtGui import *

import main
from main import ausfuehren

class Fenster(QWidget):
    def __init__(self):
        super().__init__()
        self.initMe()

    def initMe(self):
        self.btn_import=QPushButton("HCSR Import starten",self) 
        self.btn_import.move(50,110)
        self.btn_import.setGeometry(50,70,200,25) 

        self.btn_import.clicked.connect(self._importHCSR)
        self.btn_import.clicked.connect(self._call_msg)

        self.btn_import=QPushButton("HCSR Export starten",self) 
        self.btn_import.move(50,110)
        self.btn_import.setGeometry(350,70,200,25) 

        self.btn_Katalog_import=QPushButton("Katalog Import starten",self) 
        # self.btn_Katalog_import.move(50,110)
        self.btn_Katalog_import.setGeometry(650,70,200,25)   
        
        self.setGeometry(50,50, 2000, 1000)
        self.setWindowTitle("Katalogmanagement / HCSR Import") 
        self.setWindowIcon(QIcon("agkamed.jpg")) 

        self.btn_exit=QPushButton("Tool schließen",self) 
        self.btn_exit.move(50,1000) 
        self.btn_exit.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.btn_exit.setGeometry(50,1000,200,25)

        self.txt_suche=QLineEdit(self) 
        self.txt_suche.setGeometry(50,100,900,25)

        self.lstbox_hcsr=QTableWidget(self)
        self.lstbox_hcsr.setColumnCount(8)  
        self.lstbox_hcsr.setGeometry(50,150,1800,700) 

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



# def importStart():
#     main.ausfuehren()


    
# importStart()



