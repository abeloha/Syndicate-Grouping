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

    switch_allBtn = QtCore.pyqtSignal()
    switch_agencyBtn = QtCore.pyqtSignal(int,int)
    switch_sessionBtn = QtCore.pyqtSignal()

    path = "database/"
    db_file = path + "jaji_grouping.db"
    
    if __name__ == '__main__':
        if(not fn.check_path_exists(db_file)):
            print ('Welcome. This is your first use after installation. We have set up your database. Enjoy')
            fn.assure_path_exists(path)
            db.create_db(db_file)

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('ui/mainwindow.ui', self)
       
        self.agencyBtn = self.findChild(QtWidgets.QPushButton, 'agencyBtn')
        self.agencyBtn.clicked.connect(self.agencyBtnPressed) 

        self.sessionBtn = self.findChild(QtWidgets.QPushButton, 'sessionBtn')
        self.sessionBtn.clicked.connect(self.sessionBtnPressed) 

        self.allBtn = self.findChild(QtWidgets.QPushButton, 'allBtn')
        self.allBtn.clicked.connect(self.allBtnPressed) 

        self.change_password = self.findChild(QtWidgets.QPushButton, 'change_passwordBtn')
        self.change_password.clicked.connect(self.change_passwordButtonPressed)

        show_change_password = self.check_account_user('user')

        if not show_change_password:
            self.change_password.hide()

        self.current_session_id = 0;
        self.current_session_name = '';
        
        self.label_session_name = self.findChild(QtWidgets.QLabel, 'label_session_name')
        self.get_current_session()
       

    def get_current_session(self):
        conn = db.create_connection(self.db_file)
        if conn is not None:
            with conn:
                self.current_session_id, self.current_session_name = db.get_sessions_current(conn)
                self.label_session_name.setText("Current Term: " + str(self.current_session_name))
        else:
            db.conn_error_handle()

    def agencyBtnPressed(self):
        if (not self.check_current_session()):
            return

        self.switch_agencyBtn.emit(0,0)

    def sessionBtnPressed(self):
        self.switch_sessionBtn.emit()

    def allBtnPressed(self):
        if (not self.check_current_session()):
            return

        self.switch_allBtn.emit()

    def change_passwordButtonPressed(self):
        text, okPressed = QInputDialog.getText(self, "Current Password","Enter Current Password:", QLineEdit.Password, "")
        if okPressed:
            if (text != ''):
                auth = self.check_password(str(text))
                if auth:
                    self.get_new_password()
                else:
                    self.show_message('Wrong Password', 'The password you entered is incorrect')
            else:
                self.show_message('No password entered', 'No value entered. You must enter a password')

    def get_new_password(self):
        text, okPressed = QInputDialog.getText(self, "New Password","Enter New Password:", QLineEdit.Password, "")
        if okPressed:
            if (text != ''):
                auth = self.check_password_match(str(text))
                if auth:
                    self.perform_change_password(text)
                    self.show_message('Success', 'Your password has been changed successfully! \nUse new password for next login')
                else:
                    self.show_message('Password not match', 'The New password does not match')
            else:
                self.show_message('No password entered', 'No value entered. You must enter a new password')

    def check_password_match(self, password):
        text, okPressed = QInputDialog.getText(self, "Confirm Password","Confirm New Password:", QLineEdit.Password, "")
        if okPressed:
            if (text == password):
                return 1        
        return 0

    def check_password(self,password):
        data = ()
        conn = db.create_connection(self.db_file)
        if conn is not None:
            with conn:
                data = db.get_account(conn)
        else:
            db.conn_error_handle()

        
        for d in data:
           if (d[2] == password):
                return 1

        return 0

    def perform_change_password(self, password): 
        conn = db.create_connection(self.db_file)
        if conn is not None:
            with conn:
                data = db.update_account(conn,password)
        else:
            db.conn_error_handle()

        return data

    def show_message(self, title, text):
        msg = QMessageBox()
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setIcon(QMessageBox.Information)
        msg.setStyleSheet("background-color: rgb(0, 0, 0);")
        msg.setStyleSheet("color: black;")
        msg.exec_()

    def check_account_user(self,user_type):
        data = ()
        conn = db.create_connection(self.db_file)
        if conn is not None:
            with conn:
                data = db.get_account(conn)
        else:
            db.conn_error_handle()

        
        for d in data:
           if (d[1] == user_type):
                return 1

        return 0

    def check_current_session(self):
        self.get_current_session()
        if(self.current_session_id):
            return 1
        
        self.show_message('Set current term', 'Please set current term first.\n\nClick MANAGE TERM to do so')
        return 0
