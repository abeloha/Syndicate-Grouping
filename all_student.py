#from PyQt5 import QtWidgets, uic
import sys, copy
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QFileDialog,QHeaderView,  QApplication,  QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QInputDialog, QLineEdit
from PyQt5.QtGui import QBrush, QColor

import engine.databaseFunction as db
import engine.generalfunction as fn
import engine.groupingFunction as gr

import sqlite3
from random import shuffle

import student as studentEdit

class Ui(QtWidgets.QDialog):

    path = "database/"
    db_file = path + "jaji_grouping.db"
    students_data = ()
    agency_name = []
    agency_id = []
    
    if __name__ == '__main__':
        if(not fn.check_path_exists(db_file)):
            print ('Welcome. This is your first time to run')
            fn.assure_path_exists(path)
            db.create_db(db_file)

    def __init__(self, param_course, param_term):
        super(Ui, self).__init__()
        uic.loadUi('ui/all_students.ui', self)

        self.current_session_id = 0
        self.current_session_name = 'current'
        self.course = param_course
        self.term = param_term

        self.get_current_session()

        self.number_of_records = 0

        self.table_area = self.findChild(QtWidgets.QScrollArea, 'table_area')

        course_name = ''
        if(param_course == 1):
            course_name = ' - Junior Course'
        else:
            course_name = ' - Senior Course'

        self.course_name = course_name

        self.label_title = self.findChild(QtWidgets.QLabel, 'label_title')
        self.label_title.setText('<html><head/><body><p><span style=" font-size:12pt; font-weight:600; color:#aa0000;">' + str(self.current_session_name) + course_name + ' Students (Term '+ str(self.term + 1) +') </span></p></body></html>')
        
        #inputs
        self.number_of_groups_text = self.findChild(QtWidgets.QLineEdit, 'txtNG')
        self.number_of_students_text = self.findChild(QtWidgets.QLineEdit, 'txtNS')

        self.exportBtn = self.findChild(QtWidgets.QPushButton, 'exportBtn') 
        self.exportBtn.clicked.connect(self.exportButtonPressed) 

       
        self.groupBtn = self.findChild(QtWidgets.QPushButton, 'groupBtn') 
        self.groupBtn.clicked.connect(self.groupButtonPressed)

        self.label_progress = self.findChild(QtWidgets.QLabel, 'label_progress')
        self.label_progress.hide()

        self.students_number_per_group = {}
        self.Groups = []

    def get_current_session(self):
        conn = db.create_connection(self.db_file)
        if conn is not None:
            with conn:
                self.current_session_id, self.current_session_name = db.get_sessions_current(conn)
        else:
            db.conn_error_handle()

    def show_all_data(self):
        self.label_progress.show()
        self.label_progress.setText('Loading...')
        self.load_agencies()
        data = self.load_students()
        self.number_of_records = len(data)
        self.students_data = data
        self.creating_tables(data)
    
    def load_agencies(self):
        data = ()
        self.agency_id = []
        self.agency_name = []

        conn = db.create_connection(self.db_file)
        if conn is not None:
            with conn:
                data = db.get_agency(conn, self.current_session_id)
                for d in data:
                    self.agency_id.append(d[0])
                    self.agency_name.append(d[1])

        else:
            db.conn_error_handle()  

    def load_students(self):
        data = ()
        conn = db.create_connection(self.db_file)
        if conn is not None:
            with conn:
                data = db.get_students_by_session(conn, self.current_session_id, self.course, self.term)
        else:
            db.conn_error_handle()

        return data
              
    def creating_tables(self, data):
        self.tableWidget = QTableWidget()        
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(11)
        self.tableWidget.setHorizontalHeaderLabels(("id;S/N;Rank;Name;SVC No;Syndicate;Grade;Corps;Sex;Country;Service").split(";"))
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)
        self.tableWidget.setColumnHidden(0,True)          
        group = ''
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
            syn = d[14]
            
            agency_indx = self.agency_id.index(d[10])
            agency = "Unknown"
            if (len(self.agency_name) > agency_indx):
                agency = self.agency_name[agency_indx]

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

                item_agency = QTableWidgetItem(str(agency))
                item_agency.setBackground(QBrush(QColor(255, 0, 0)))
                item_agency.setForeground(QBrush(QColor(255, 255, 255)))
                self.tableWidget.setItem(c, 10 , (item_agency))

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
                self.tableWidget.setItem(c, 10 , QTableWidgetItem(str(agency))) 

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

    def groupButtonPressed(self):
        num_groups = self.number_of_groups_text.text()
        num_students = self.number_of_students_text.text()
        val = 0
        
        if(not self.number_of_records):
            QMessageBox.warning(self, "Error", "No student records in the system. \n\nYou must add some records before grouping")
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
        
        self.Groups = [[] for i in range(number_of_groups)]
        self.students_number_per_group = {}
        
        for i in range(number_of_groups):
            self.students_number_per_group[i] = 0

        conn = db.create_connection(self.db_file)
        if conn is not None:
            with conn:
                for agency in self.agency_id:
                    agency_students = db.get_students_by_agency(conn, agency, self.course, self.term)
                    groups = gr.perform_grouping(agency_students,number_of_groups)
                    self.grouping_merge_controller(groups)
                    
        else:
            db.conn_error_handle()        
         
        self.update_grouping(self.Groups)
        num = number_of_groups
        if(num):
           self.show_message("Success", "The students has been grouped into " + str(num) + " syndicates")

        else:
            QMessageBox.warning(self, "Info", "Grouping failed.")

        self.show_all_data()

    def grouping_merge_controller(self,groups):
        
        sGroup = sorted(groups, key=len)       
        number_of_groups = len(sGroup)

        st = sorted(self.students_number_per_group.items(), key=lambda x: x[1], reverse=True)
       
        for i in range(number_of_groups):
            x, y = st[i] #x = index, y = value

            self.grouping_merge(x, sGroup[i])
            self.students_number_per_group[x] += len(sGroup[i])

    def grouping_merge(self, i, group):
        for member in group:
            self.Groups[i].append(member)

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
            sql = "UPDATE students SET group_triservice_no = " + str(syn) + " WHERE id IN {}".format(value)
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
                    SET group_triservice_no = ? 
                    WHERE dept_id IN (
                        SELECT id FROM depts 
                        WHERE is_deleted = 0 AND session_id = ?
                    )"""        
        
        values = (0, self.current_session_id)
        # Execute sql Query
        cur.execute(sql, values)
        
    def exportButtonPressed(self):

        data = self.students_data
        if (not len(data)):
            QMessageBox.warning(self, "Error", "No student records in the system. \n\nYou must add some records before exporting.")
            return

        filename = self.selectSaveFileNameDialog()
        if (not filename):
            QMessageBox.warning(self, "Info", "No file directory is selected \nYou must select the directory to export data to.")
            return 

        title = str(self.current_session_name) + self.course_name + ' Students (Term '+ str(self.term + 1) +')'
        k = gr.print_to_doc(data,filename, title, 2)

        if(k):
            self.show_message("Success", "The syndicates for this service has been saved successfully in \n" + str(filename) + '.docx')
        else:
            QMessageBox.warning(self, "Failed", "Exporting failed. You may have supplied invalid file name or chosen a path without write access. Try again")
        
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
    controller = Ui(1, 0)
    controller.show()
    controller.show_all_data()
    sys.exit(app.exec_())

#runapp()