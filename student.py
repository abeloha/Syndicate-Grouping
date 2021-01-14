#from PyQt5 import QtWidgets, uic
import sys, copy
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QApplication, QHeaderView,  QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QInputDialog, QLineEdit
from PyQt5.QtGui import QBrush, QColor

import engine.databaseFunction as db
import engine.generalfunction as fn
import engine.groupingFunction as gr

from datetime import datetime

import sqlite3
import xlrd

from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH


class Ui(QtWidgets.QDialog):

    signal_edited = QtCore.pyqtSignal()

    path = "database/"
    db_file = path + "jaji_grouping.db"
      
    if __name__ == '__main__':
        if(not fn.check_path_exists(db_file)):
            print ('Welcome. This is your first use after installation. We have set up your database. Enjoy')
            fn.assure_path_exists(path)
            db.create_db(db_file)

    def __init__(self, param_id, parent=None):
        super(Ui, self).__init__()
        uic.loadUi('ui/student.ui', self)

        self.student_id = param_id
            
        #inputs
        self.txtrank = self.findChild(QtWidgets.QLineEdit, 'txtrank')
        self.txtname = self.findChild(QtWidgets.QLineEdit, 'txtname')

        self.txtno = self.findChild(QtWidgets.QLineEdit, 'txtno')
        self.txtcountry = self.findChild(QtWidgets.QLineEdit, 'txtcountry')

        self.txtspeciality = self.findChild(QtWidgets.QLineEdit, 'txtspeciality')
        self.txtgender = self.findChild(QtWidgets.QLineEdit, 'txtgender')

        self.txtgrade = self.findChild(QtWidgets.QLineEdit, 'txtgrade')
        self.txtremarks = self.findChild(QtWidgets.QLineEdit, 'txtremarks')

        self.txtssyn = self.findChild(QtWidgets.QLineEdit, 'txtssyn')
        self.txttsyn = self.findChild(QtWidgets.QLineEdit, 'txttsyn')


        self.saveBtn = self.findChild(QtWidgets.QPushButton, 'saveBtn') 
        self.saveBtn.clicked.connect(self.saveButtonPressed) 

        self.load_student()

    def load_student(self):
        data = ()
        conn = db.create_connection(self.db_file)
        if conn is not None:
            with conn:
                data = db.get_students(conn, self.student_id)
        else:
            db.conn_error_handle()

        if (data):
            for d in data:
                self.pupulate_input(d)

    def pupulate_input(self, d):
        id = d[0]
        rank = d[2]
        name = d[3]
        p_no = d[4]
        country = d[5]
        gender = d[6]
        grade = d[7]
        specialty = d[8]
        remarks = d[9]
        ssyn = d[13]
        tsyn = d[14]

        self.txtrank.setText(str(rank))
        self.txtname.setText(str(name))

        self.txtno.setText(str(p_no))
        self.txtcountry.setText(str(country)) 

        self.txtspeciality.setText(str(specialty))
        self.txtgender.setText(str(gender))

        self.txtgrade.setText(str(grade))
        self.txtremarks.setText(str(remarks)) 

        self.txtssyn.setText(str(ssyn))
        self.txttsyn.setText(str(tsyn)) 

    def saveButtonPressed(self):
        rank =self.txtrank.text()
        name = self.txtname.text()
        p_no = self.txtno.text()
        country = self.txtcountry.text()
        gender = self.txtgender.text()
        grade = self.txtgrade.text()
        specialty = self.txtspeciality.text()
        remarks = self.txtremarks.text()
        ssyn = self.txtssyn.text()
        tsyn = self.txttsyn.text()

        valssyn = 0
        valtsyn = 0

        if(ssyn):
            try:
                valssyn = int(ssyn)
            except ValueError:
                QMessageBox.warning(self, "Error", "The value of single service syndicate must be a valid INTEGR NUMBER")
                return

        if(tsyn):
            try:
                valtsyn = int(tsyn)
            except ValueError:
                QMessageBox.warning(self, "Error", "The value of single service syndicate must be a valid INTEGR NUMBER")
                return

        data = (rank, name, p_no, country, gender, grade, specialty, remarks, valssyn, valtsyn, self.student_id)
        conn = db.create_connection(self.db_file)
        if conn is not None:                
            with conn:
                db.update_student(conn, data)   
                self.show_message('Successful', 'Changes has been saved')  
                self.signal_edited.emit()       
        else:
            db.conn_error_handle()

        self.load_student()

        '''
        text, okPressed = QInputDialog.getText(self, "Confirmation","Grouping the records will delete any previous groups!! \n\nType any text and click OK to confirm this action. Otherwise, click cancel", QLineEdit.Normal, "")
        if okPressed:
            if(text):
               self.perform_grouping(val)
        '''

    def perform_save(self, data):
        pass

    def show_message(self, title, text):
        msg = QMessageBox()
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setIcon(QMessageBox.Information)
        msg.setStyleSheet("background-color: rgb(0, 0, 0);")
        msg.setStyleSheet("color: black;")
        msg.exec_()

def runapp():
    app = QtWidgets.QApplication(sys.argv)
    controller = Ui(1)
    controller.show()
    sys.exit(app.exec_())

#runapp()