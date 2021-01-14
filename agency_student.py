#from PyQt5 import QtWidgets, uic
import sys, copy
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QApplication, QHeaderView,  QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QInputDialog, QLineEdit
from PyQt5.QtGui import QBrush, QColor

import engine.databaseFunction as db
import engine.generalfunction as fn
import engine.groupingFunction as gr

from random import shuffle

import sqlite3
import xlrd

import student as studentEdit

class Ui(QtWidgets.QDialog):

    path = "database/"
    db_file = path + "jaji_grouping.db"
    students_data = ()
    
    if __name__ == '__main__':
        if(not fn.check_path_exists(db_file)):
            print ('Welcome. This is your first use after installation. We have set up your database. Enjoy')
            fn.assure_path_exists(path)
            db.create_db(db_file)

    def __init__(self, param_id, param_name = 'unkown', param_course = 0, param_term = 0, param_do_grouping = 0):
        super(Ui, self).__init__()
        uic.loadUi('ui/agency_students.ui', self)

        self.agency_id = param_id
        self.agency_name = param_name
        self.term = param_term
        self.course = param_course
        self.do_grouping = param_do_grouping

        course_name = '';
        if(param_course == 1):
            course_name = ' - Junior Course'
        else:
            course_name = ' - Senior Course'

        self.course_name = course_name

        self.number_of_records = 0

        self.table_area = self.findChild(QtWidgets.QScrollArea, 'table_area')

        self.label_agency_name = self.findChild(QtWidgets.QLabel, 'label_agency_name')
        self.label_agency_name.setText('<html><head/><body><p><span style=" font-size:12pt; font-weight:600; color:#aa0000;">' + self.agency_name + course_name + ' Students (Term '+ str(self.term + 1) +') </span></p></body></html>')
            
        #inputs
        self.number_of_groups_text = self.findChild(QtWidgets.QLineEdit, 'txtNG')
        self.number_of_students_text = self.findChild(QtWidgets.QLineEdit, 'txtNS')

        self.addBtn = self.findChild(QtWidgets.QPushButton, 'addBtn') 
        self.addBtn.clicked.connect(self.addButtonPressed) 

        self.exportBtn = self.findChild(QtWidgets.QPushButton, 'exportBtn') 
        self.exportBtn.clicked.connect(self.exportButtonPressed) 

        self.deleteBtn = self.findChild(QtWidgets.QPushButton, 'deleteBtn') 
        self.deleteBtn.clicked.connect(self.deleteButtonPressed)

        self.groupBtn = self.findChild(QtWidgets.QPushButton, 'groupBtn') 
        self.groupBtn.clicked.connect(self.groupButtonPressed)

        self.label_progress = self.findChild(QtWidgets.QLabel, 'label_progress')
        self.label_progress.hide()

        self.groupBox = self.findChild(QtWidgets.QGroupBox, 'groupBox')
        self.groupBox_sample = self.findChild(QtWidgets.QGroupBox, 'groupBox_sample')
        self.groupBox_group_inst = self.findChild(QtWidgets.QGroupBox, 'groupBox_group_inst')

        if (param_do_grouping == 0):
            self.exportBtn.hide()
            self.groupBox.hide()
            self.groupBox_sample.show()            
            self.groupBox_group_inst.hide()
        else:
            self.deleteBtn.hide()
            self.addBtn.hide()
            self.groupBox_sample.hide()
            self.groupBox_group_inst.show()

    def show_all_data(self):
        self.label_progress.show()
        self.label_progress.setText('Loading...')
        data = self.load_students()
        self.number_of_records = len(data)
        self.students_data = data
        self.creating_tables(data)
    
    def load_students(self):
        data = ()
        conn = db.create_connection(self.db_file)
        if conn is not None:
            with conn:
                data = db.get_students_by_agency(conn, self.agency_id, self.course, self.term)
        else:
            db.conn_error_handle()

        return data
              
    def creating_tables(self, data):
        self.tableWidget = QTableWidget()        
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setHorizontalHeaderLabels(("id;S/N;Rank;Name;SVC No;Syndicate;Grade;Corps;Sex;Country").split(";"))
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)
        self.tableWidget.setColumnHidden(0,True)          
        group = '';
        c = 0
        sn = 1

        reverse = False

        for d in data:
            id = d[0]
            rank = d[2]
            name = d[3]
            p_no = d[4]
            country = d[5]
            gender = d[6]
            grade = d[7]
            specialty = d[8]
            remarks = d[9]
            syn = d[13]
            if (syn == 0):
                syn = "NONE"
            
            if(group != syn):                
                group = syn                
                sn = 1
                reverse = not reverse
            
            if(reverse):  
                self.tableWidget.setItem(c, 0 , QTableWidgetItem(str(id)))

                item_sn = QTableWidgetItem(str(sn))
                item_sn.setBackground(QBrush(QColor(255, 0, 0)))
                item_sn.setForeground(QBrush(QColor(255, 255, 255)))
                self.tableWidget.setItem(c, 1 , (item_sn))

                item_rank = QTableWidgetItem(str(rank))
                item_rank.setBackground(QBrush(QColor(255, 0, 0)))
                item_rank.setForeground(QBrush(QColor(255, 255, 255)))
                self.tableWidget.setItem(c, 2 , (item_rank))

                item_name = QTableWidgetItem(str(name))
                item_name.setBackground(QBrush(QColor(255, 0, 0)))
                item_name.setForeground(QBrush(QColor(255, 255, 255)))
                self.tableWidget.setItem(c, 3 , (item_name))

                item_p_no = QTableWidgetItem(str(p_no))
                item_p_no.setBackground(QBrush(QColor(255, 0, 0)))
                item_p_no.setForeground(QBrush(QColor(255, 255, 255)))
                self.tableWidget.setItem(c, 4 , (item_p_no))

                item_syn = QTableWidgetItem(str(syn))
                item_syn.setBackground(QBrush(QColor(255, 0, 0)))
                item_syn.setForeground(QBrush(QColor(255, 255, 255)))
                self.tableWidget.setItem(c, 5 , (item_syn))

                item_grade = QTableWidgetItem(str(grade))
                item_grade.setBackground(QBrush(QColor(255, 0, 0)))
                item_grade.setForeground(QBrush(QColor(255, 255, 255)))
                self.tableWidget.setItem(c, 6 , (item_grade))

                item_specialty = QTableWidgetItem(str(specialty))
                item_specialty.setBackground(QBrush(QColor(255, 0, 0)))
                item_specialty.setForeground(QBrush(QColor(255, 255, 255)))
                self.tableWidget.setItem(c, 7 , (item_specialty))

                item_gender = QTableWidgetItem(str(gender))
                item_gender.setBackground(QBrush(QColor(255, 0, 0)))
                item_gender.setForeground(QBrush(QColor(255, 255, 255)))
                self.tableWidget.setItem(c, 8 , (item_gender))

                item_country = QTableWidgetItem(str(country))
                item_country.setBackground(QBrush(QColor(255, 0, 0)))
                item_country.setForeground(QBrush(QColor(255, 255, 255)))
                self.tableWidget.setItem(c, 9 , (item_country))

            else:              
                self.tableWidget.setItem(c, 0 , QTableWidgetItem(str(id)))
                self.tableWidget.setItem(c, 1 , QTableWidgetItem(str(sn)))
                self.tableWidget.setItem(c, 2 , QTableWidgetItem(str(rank)))
                self.tableWidget.setItem(c, 3 , QTableWidgetItem(str(name)))
                self.tableWidget.setItem(c, 4 , QTableWidgetItem(str(p_no)))
                self.tableWidget.setItem(c, 5 , QTableWidgetItem(str(syn)))
                self.tableWidget.setItem(c, 6 , QTableWidgetItem(str(grade)))
                self.tableWidget.setItem(c, 7 , QTableWidgetItem(str(specialty)))
                self.tableWidget.setItem(c, 8 , QTableWidgetItem(str(gender)))
                self.tableWidget.setItem(c, 9 , QTableWidgetItem(str(country)))  

            c+=1
            sn += 1
        
         # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)
        
        self.table_area.setWidget(self.tableWidget)

        if(len(data) == 0):
            self.label_progress.setText('No students yet')
        else:
            self.label_progress.setText('')
            self.label_progress.hide()

    def on_click(self):
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            row = currentQTableWidgetItem.row()

        item = self.tableWidget.item(row, 0)
        id = int(item.text())

        self.show_student_edit(id)

    def addButtonPressed(self):
        filename = self.selectFileNameDialog()
        if (not filename):
            QMessageBox.warning(self, "Info", "No excel file is selected \nStudents can only be imported into the database from an excel file.")
            return 

        num = self.addStudentsFromFile(filename)

        self.show_all_data()

        if(num):
           self.show_message("Success", str(num) + " records have been successfully uploaded")

        else:
            QMessageBox.warning(self, "Info", "No record is inserted.")
  
    def selectFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Select an Excel File", "","Excel Files (*.xls);;Excel Files (*.xlsx)", options=options)
        return fileName
           
    def selectSaveFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Choose location to save file", "","Word Files (*.doc);;Word Files (*.docx)", options=options)
        return fileName

    def addStudentsFromFile(self, fileName):
        num = 0
        
        # Open the workbook and define the worksheet
        book = xlrd.open_workbook(fileName)
        sheet = book.sheet_by_index(0)

        # Create the INSERT INTO sql query
        sql = """INSERT INTO students 
                    (serial, rank, name, p_no, country, gender, grade, specialty, remarks, dept_id, course, term) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

        conn = db.create_connection(self.db_file)
        if conn is not None:
            with conn:
                cur = conn.cursor()                    
                # Create a For loop to iterate through each row in the XLS file, starting at row 2 to skip the headers
                for r in range(1, sheet.nrows):
                    serial		= sheet.cell(r,0).value
                    rank	    = sheet.cell(r,1).value
                    name		= sheet.cell(r,2).value
                    p_no		= sheet.cell(r,3).value
                    country		= sheet.cell(r,4).value
                    specialty	= sheet.cell(r,5).value
                    gender		= sheet.cell(r,6).value
                    grade		= sheet.cell(r,7).value
                    remarks	    = sheet.cell(r,8).value

                    # Assign values from each row
                    values = (serial, rank, name, p_no, country, gender, grade, specialty, remarks, self.agency_id, self.course, self.term)

                    # Execute sql Query
                    cur.execute(sql, values)

                    num += 1
        else:
            db.conn_error_handle()

            
        
        return num
        
    def deleteButtonPressed(self):
        text, okPressed = QInputDialog.getText(self, "Password","Deleting records cannot be UNDONE! \n\nTHIS CANNOT BE UNDONE!! \n\nEnter password to procceed:", QLineEdit.Password, "")
        if okPressed:
            if (text != ''):
                auth = self.check_password(str(text))
                if auth:
                    conn = db.create_connection(self.db_file)
                    if conn is not None:
                        with conn:
                            cur = conn.cursor()
                            cur.execute('DELETE FROM students WHERE dept_id = '+str(self.agency_id) + ' AND course = '+str(self.course)+ ' AND term = '+str(self.term))                            
                            self.show_message('Sucessful', 'All records has been deleted')
                            self.show_all_data()                         
                    else:
                        db.conn_error_handle()
                        QMessageBox.warning(self, "Failed", "Sorry, the record cannot be deleted now")

                else:
                    self.show_message('Wrong Password', 'The password you entered is incorrect')
            else:
                self.show_message('No password entered', 'No value entered. You must enter a password to delete records')

    def groupButtonPressed(self):
        num_groups = self.number_of_groups_text.text()
        num_students = self.number_of_students_text.text()
        val = 0

        if(not self.number_of_records):
            QMessageBox.warning(self, "Error", "No student records in the system. \n\n You must add some records before grouping")
            return

        if((not num_groups and not num_students) or (num_groups and num_students)):
            QMessageBox.warning(self, "Error", "You must enter either the number of groups to divide the students into or the number of students for each group.\n\nBUT DO NOT ENTER BOTH")
            return

        if(num_groups):
            try:
                val = int(num_groups)
            except ValueError:
                QMessageBox.warning(self, "Error", "The number of groups must be a valid INTEGR NUMBER")
                return
        else:
            try:
                vals = int(num_students)
                val = round(self.number_of_records/vals)
            except ValueError:
                QMessageBox.warning(self, "Error", "The number of students for each group must be a valid INTEGR NUMBER")
                return
        
        text, okPressed = QInputDialog.getText(self, "Confirmation","Grouping the records will delete any previous groups!! \n\nType any text and click OK to confirm this action. Otherwise, click cancel", QLineEdit.Normal, "")
        if okPressed:
            if(text):
               self.perform_grouping(val)

    def perform_grouping(self, number_of_groups = 0):
        if (not number_of_groups):
            number_of_groups = 1
        
        if(not self.number_of_records):
            QMessageBox.warning(self, "Error", "No student records in the system. \n\nYou must add some records before grouping")
            return
        
        groups = gr.perform_grouping(self.students_data,number_of_groups)
        
        num = self.update_grouping(groups)
        if(num):
           self.show_message("Success", "The students has been grouped into " + str(num) + " syndicates")

        else:
            QMessageBox.warning(self, "Info", "Grouping failed.")

        self.show_all_data()
    
    def update_grouping(self,groups):
        number_of_groups = len(groups)
        
        group_names = list(range(1,number_of_groups + 1))
        shuffle (group_names)
         
        for i in range(number_of_groups):
            ids = []
            for member in groups[i]:
                ids.append(member.id)
            
            value = tuple(ids)
            syn = group_names[i]
            sql = "UPDATE students SET group_no = " + str(syn) + " WHERE id IN {}".format(value)
            conn = db.create_connection(self.db_file)
            if conn is not None:
                with conn:
                    cur = conn.cursor()
                    cur.execute(sql)
            else:
                db.conn_error_handle()
            
        return number_of_groups

    def clear_grouping(self, conn):
        cur = conn.cursor() 
        sql = """UPDATE students
                    SET group_no = ? 
                    WHERE dept_id = ? """        
        
        values = (0, self.agency_id)
        # Execute sql Query
        cur.execute(sql, values)
       
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

    def exportButtonPressed(self):

        data = self.students_data
        if (not len(data)):
            QMessageBox.warning(self, "Error", "No student records in the system. \n\nYou must add some records before exporting.")
            return

        filename = self.selectSaveFileNameDialog()
        if (not filename):
            QMessageBox.warning(self, "Info", "No file directory is selected \nYou must select the directory to export data to.")
            return 

        title = self.agency_name + self.course_name + ' Students (Term '+ str(self.term + 1) +')'
        k = gr.print_to_doc(data,filename, title, 1)

        if(k):
            self.show_message("Success", "The syndicates for this service has been saved successfully in \n" + str(filename) + '.docx')
        else:
            QMessageBox.warning(self, "Failed", "Exporting failed. Try again")
            

    def show_message(self, title, text):
        msg = QMessageBox()
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setIcon(QMessageBox.Information)
        msg.setStyleSheet("background-color: rgb(0, 0, 0);")
        msg.setStyleSheet("color: black;")
        msg.exec_()

    def show_student_edit(self, id):
        self.edit_student_ui = studentEdit.Ui(id)
        self.edit_student_ui.signal_edited.connect(self.student_edited)
        self.edit_student_ui.show()

    def student_edited(self): 
        self.show_all_data();

def runapp():
    app = QtWidgets.QApplication(sys.argv)
    controller = Ui(1, 'Test', 1, 0, 1)
    controller.show()
    controller.show_all_data()
    sys.exit(app.exec_())

#runapp()