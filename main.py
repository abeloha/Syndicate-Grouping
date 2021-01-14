#Developed Started May 1, 2020 ented May 3, 2020. Redesigned from 22
import sys
from PyQt5 import QtCore, QtWidgets
import engine.generalfunction as fn
import engine.databaseFunction as db
import login
import menu
import course
import session
import agency
import agency_student
import all_student

class Controller:

    path = "database/"
    db_file = path + "jaji_grouping.db"
    
    if __name__ == '__main__':
        if(not fn.check_path_exists(db_file)):
            print ('Welcome. This is your first use after installation. We have set up your database. Enjoy')
            fn.assure_path_exists(path)
            db.create_db(db_file)

    def __init__(self):
        pass

    def show_login(self):
        self.login = login.Ui()
        self.login.switch_window.connect(self.show_menu)
        self.login.show()

    def show_menu(self):
        self.menu = menu.Ui()
        self.menu.switch_sessionBtn.connect(self.show_session)
        self.menu.switch_course.connect(self.show_course)
        self.login.close()
        self.menu.show()

    def show_course(self,course_type):
        self.course = course.Ui(course_type)        
        self.course.switch_dept.connect(self.show_agency)
        self.course.switch_all_student_list.connect(self.show_all_students)
        self.course.show()

    def show_session(self):
        self.session = session.Ui()
        self.session.show()
        self.session.show_all_data()

    def show_agency(self, course, term, do_grouping):
        self.agency = agency.Ui(course, term, do_grouping)
        self.agency.switch_agency_students.connect(self.show_agency_students)
        self.agency.show()
        self.agency.show_all_data()

    def show_agency_students(self,id,name, course, term, do_grouping):
        self.agency_student = agency_student.Ui(id, name, course, term, do_grouping)
        self.agency_student.show()
        self.agency_student.show_all_data()

    def show_all_students(self, course, term):
        self.all_student = all_student.Ui(course, term)
        self.all_student.show()
        self.all_student.show_all_data()
   
def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_login()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()