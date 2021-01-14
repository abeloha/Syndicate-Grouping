#from PyQt5 import QtWidgets, uic
import sys
from PyQt5 import QtWidgets, uic, QtGui, QtCore

#input dialog
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFileDialog 
import engine.databaseFunction as db
import engine.generalfunction as fn
from datetime import datetime

class Ui(QtWidgets.QDialog):

    switch_dept = QtCore.pyqtSignal(int,int,int) #course, term, do_grouping
    switch_all_student_list = QtCore.pyqtSignal(int,int) #course, term

    path = "database/"
    db_file = path + "jaji_grouping.db"
    
    if __name__ == '__main__':
        if(not fn.check_path_exists(db_file)):
            print ('Welcome. This is your first use after installation. We have set up your database. Enjoy')
            fn.assure_path_exists(path)
            db.create_db(db_file)

    def __init__(self, param_course):
        super(Ui, self).__init__()
        uic.loadUi('ui/course.ui', self)

        self.groupBtn = self.findChild(QtWidgets.QPushButton, 'groupBtn')
        self.groupBtn.clicked.connect(self.groupBtnPressed)

        self.recordBtn = self.findChild(QtWidgets.QPushButton, 'recordBtn')
        self.recordBtn.clicked.connect(self.recordBtnPressed)

        self.comboTerms = self.findChild(QtWidgets.QComboBox, 'comboTerms')
        self.comboTerms.currentIndexChanged.connect(self.termSelected)

        self.label_title = self.findChild(QtWidgets.QLabel, 'label_title')
        self.label_syn = self.findChild(QtWidgets.QLabel, 'label_syn')

        if(param_course == 1):
            self.label_title.setText('<html><head/><body><p align="center"><span style=" font-size:28pt; font-weight:600; color:#ffffff;">Junior Course</span></p></body></html>')
        else: 
            self.label_title.setText('<html><head/><body><p align="center"><span style=" font-size:28pt; font-weight:600; color:#ffffff;">Senior Course</span></p></body></html>')
            
        self.course = param_course

        self.syndicate_type = 0;
        self.term = 0;

        self.populateTerms()

    def groupBtnPressed(self):
        if (self.syndicate_type == 0):
            self.showDept(1)
        else:
           self.switch_all_student_list.emit(self.course, self.term)


    def recordBtnPressed(self):
        self.showDept(0)

    def showDept(self, do_grouping = 0):
         self.switch_dept.emit(self.course, self.term, do_grouping)

    def populateTerms(self):
        if(self.course == 1):
            self.comboTerms.addItems(["Term 1", "Term 2"])
        else:
            self.comboTerms.addItems(["Term 1", "Term 2", "Term 3", "Term 4", "Term 5"])

    def termSelected(self):
        term = self.comboTerms.currentIndex()
        self.setSyndicateType(term)
    
    def setSyndicateType(self, term):
        syn_type = 0

        if(self.course==1):
            if(term > 1):
                term = 0

            type_list = (1,0)
            name_list = ('Tri-Service', 'Single Service')
            syn_name = name_list[term]
            syn_type = type_list[term]
        
        if(self.course==2):
            if(term > 4):
                term = 0

            type_list = (1,0,0,1,1)
            name_list = ('Tri-Service', 'Single Service', 'Single Service', 'Tri-Service', 'Tri-Service')
            syn_name = name_list[term]
            syn_type = type_list[term]


        self.term = term
        self.syndicate_type = syn_type
        self.setLabelSyn(syn_name)

    def setLabelSyn(self, name):
        self.label_syn.setText('<html><head/><body><p align="center"><span style=" font-size:16pt; font-weight:600; color:#ffffff;">' + str(name) + ' Syndicate</span></p></body></html>')
            
    def show_message(self, title, text):
        msg = QMessageBox()
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setIcon(QMessageBox.Information)
        msg.setStyleSheet("background-color: rgb(0, 0, 0);")
        msg.setStyleSheet("color: black;")
        msg.exec_()
