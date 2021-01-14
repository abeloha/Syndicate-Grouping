#from PyQt5 import QtWidgets, uic
import sys, copy
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QApplication,  QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
import engine.databaseFunction as db
import engine.generalfunction as fn

from datetime import datetime

class Ui(QtWidgets.QDialog):

    switch_agency_students = QtCore.pyqtSignal(int, str, int, int, int) #id,name, course, term, do_grouping

    path = "database/"
    db_file = path + "jaji_grouping.db"
    
    if __name__ == '__main__':
        if(not fn.check_path_exists(db_file)):
            print ('Welcome. This is your first use after installation. We have set up your database. Enjoy')
            fn.assure_path_exists(path)
            db.create_db(db_file)

    def __init__(self, param_course, param_term, param_do_grouping = 0):
        super(Ui, self).__init__()
        uic.loadUi('ui/agency.ui', self)

        self.course = param_course
        self.term = param_term
        self.do_grouping = param_do_grouping

        self.current_session_id = 1;
        self.current_session_name = 'current';

        self.get_current_session()

        self.table_area = self.findChild(QtWidgets.QScrollArea, 'table_area')

        self.addBtn = self.findChild(QtWidgets.QPushButton, 'addBtn') 
        self.addBtn.clicked.connect(self.addButtonPressed) 

        self.name_text = self.findChild(QtWidgets.QLineEdit, 'name_text')
        self.label_progress = self.findChild(QtWidgets.QLabel, 'label_progress')
        self.label_title = self.findChild(QtWidgets.QLabel, 'label_title')
        
        self.label_selected_session = self.findChild(QtWidgets.QLabel, 'label_selected_session')
       
        self.label_progress.hide()

        self.setLabelTitle()

    def setLabelTitle(self):
        term_list = ("Term 1", "Term 2", "Term 3", "Term 4", "Term 5")

        if(self.course == 2):
            name = "Senior"

            if(self.term > 4):
                self.term = 0 

        else:
            name = "junior"
            self.course = 1

            if(self.term > 1):
                self.term = 0 

        term = term_list[self.term]

        self.label_title.setText('<html><head/><body><p><span style=" font-size:14pt; font-weight:600; color:#aa0000;">Services - ' + name + ' Course (' + term + ')</span></p></body></html>')
        
    def get_current_session(self):
        conn = db.create_connection(self.db_file)
        if conn is not None:
            with conn:
                self.current_session_id, self.current_session_name = db.get_sessions_current(conn)
        else:
            db.conn_error_handle()

        return 1

    def show_all_data(self):
        self.label_progress.show()
        self.label_progress.setText('Loading...')
        data = self.load_agency()
        self.creating_tables(data)

    def addButtonPressed(self):
        name_text = self.name_text.text()        
        date_created = datetime.now().strftime("%d-%m-%Y %H:%M")
        data = (name_text, self.current_session_id, date_created)
        conn = db.create_connection(self.db_file)
        if conn is not None:
            with conn:
                id = db.create_agency(conn,data)
            self.show_all_data()
        else:
            db.conn_error_handle()

    def load_agency(self):
        data = ()
        conn = db.create_connection(self.db_file)
        if conn is not None:
            with conn:
                data = db.get_agency(conn, self.current_session_id)
        else:
            db.conn_error_handle()

        return data
              
    def creating_tables(self, data):
        self.tableWidget = QTableWidget()
        
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(("id;Name;Year;Date Added;Action").split(";"))
        self.tableWidget.setColumnHidden(0,True)  
            
        c = 0
        for d in data:
            id = d[0]
            name = d[1]
           
            date = d[4]
            self.tableWidget.setItem(c, 0 , QTableWidgetItem(str(id)))
            self.tableWidget.setItem(c, 1 , QTableWidgetItem(str(name)))
            self.tableWidget.setItem(c, 2 , QTableWidgetItem(str(self.current_session_name)))
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
        id = int(item.text())

        item1 = self.tableWidget.item(row, 1)
        name = str(item1.text())

        self.switch_to_agency_students(id, name)

    def switch_to_agency_students(self, id, name):
        self.switch_agency_students.emit(id, name, self.course, self.term, self.do_grouping)

        #print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
