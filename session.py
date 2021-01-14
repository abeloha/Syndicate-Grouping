#from PyQt5 import QtWidgets, uic
import sys, copy
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QApplication,  QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
import engine.databaseFunction as db
import engine.generalfunction as fn

from datetime import datetime

class Ui(QtWidgets.QDialog):

    switch_user = QtCore.pyqtSignal(int,int)

    path = "database/"
    db_file = path + "jaji_grouping.db"
    
    if __name__ == '__main__':
        if(not fn.check_path_exists(db_file)):
            print ('Welcome. This is your first use after installation. We have set up your database. Enjoy')
            fn.assure_path_exists(path)
            db.create_db(db_file)

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('ui/session.ui', self)

        self.table_area = self.findChild(QtWidgets.QScrollArea, 'table_area')

        self.addBtn = self.findChild(QtWidgets.QPushButton, 'addBtn') 
        self.addBtn.clicked.connect(self.addButtonPressed) 

        self.makeCurrentBtn = self.findChild(QtWidgets.QPushButton, 'makeCurrentBtn') 
        self.makeCurrentBtn.clicked.connect(self.makeCurrentBtnPressed) 

        self.deleteBtn = self.findChild(QtWidgets.QPushButton, 'deleteBtn') 
        self.deleteBtn.clicked.connect(self.deleteBtnPressed) 

        self.name_text = self.findChild(QtWidgets.QLineEdit, 'name_text')
        self.label_progress = self.findChild(QtWidgets.QLabel, 'label_progress')
        
        self.label_selected_session = self.findChild(QtWidgets.QLabel, 'label_selected_session')
        self.groupBox = self.findChild(QtWidgets.QGroupBox, 'groupBox')

        self.label_progress.hide()
        self.groupBox.hide()

        self.selected_session_id = 0;

    def show_all_data(self):
        self.groupBox.hide()
        self.label_progress.show()
        self.label_progress.setText('Loading...')
        data = self.load_sessions()
        self.creating_tables(data)

    def addButtonPressed(self):
        name_text = self.name_text.text()        
        date_created = datetime.now().strftime("%d-%m-%Y %H:%M") 
        data = (name_text, date_created)
        conn = db.create_connection(self.db_file)
        if conn is not None:
            with conn:
                id = db.create_session(conn,data)
            self.show_all_data()
        else:
            db.conn_error_handle()

    def load_sessions(self):
        data = ()
        conn = db.create_connection(self.db_file)
        if conn is not None:
            with conn:
                data = db.get_sessions(conn)
        else:
            db.conn_error_handle()

        return data
              
    def creating_tables(self, data):
        self.tableWidget = QTableWidget()
        
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(("id;Name;Is Current?;Date added;action").split(";"))
        self.tableWidget.setColumnHidden(0,True)  
            
        c = 0
        for d in data:
            id = d[0]
            name = d[1]
            isc = 'No'

            if(d[2]):
                isc = 'Yes'

            date = d[4]
            self.tableWidget.setItem(c, 0 , QTableWidgetItem(str(id)))
            self.tableWidget.setItem(c, 1 , QTableWidgetItem(str(name)))
            self.tableWidget.setItem(c, 2 , QTableWidgetItem(isc))
            self.tableWidget.setItem(c, 3 , QTableWidgetItem(str(date)))
            self.tableWidget.setItem(c, 4 , QTableWidgetItem('Manage'))  
            c+=1
        
         # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)
        
        self.table_area.setWidget(self.tableWidget)

        self.label_progress.setText('')
        self.label_progress.hide()

    def on_click(self):
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            row = currentQTableWidgetItem.row()
        
        item = self.tableWidget.item(row, 0)
        self.selected_session_id = int(item.text())

        itemname = self.tableWidget.item(row, 1)
        name = str(itemname.text())

        self.label_selected_session.setText(name)
        self.groupBox.show()


        #print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

    def makeCurrentBtnPressed(self):
        conn = db.create_connection(self.db_file)
        if conn is not None:
            with conn:
                db.update_session_current(conn, self.selected_session_id, 0)
                db.update_session_current(conn, self.selected_session_id, 1)
                self.show_all_data()
        else:
            db.conn_error_handle()

       


    def deleteBtnPressed(self):
        conn = db.create_connection(self.db_file)
        if conn is not None:
            with conn:
                db.delete_session(conn, self.selected_session_id)
                self.show_all_data()
        else:
            db.conn_error_handle()  

