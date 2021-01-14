import sqlite3
from sqlite3 import Error

from datetime import datetime
import engine.generalfunction as fn

def create_connection(db_file):      
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
 
    return conn

def conn_error_handle():
    print("Error! System cannot connect to database now.")

def create_db(db_file):      
    conn = create_connection(db_file)
    if conn is not None:
        
        create_table_student(conn)
        create_table_dept(conn)
        create_table_sessions(conn)
        create_table_grouping_dept(conn)
        create_table_grouping_session(conn)
        create_table_account(conn)

        with conn:
            create_default_account(conn)
        
    else:
        conn_error_handle()

def create_table_account(conn):
    cur = conn.cursor()
    sql = """CREATE TABLE account (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        name     TEXT    DEFAULT trial,
        password TEXT    DEFAULT AFCSC,
        trial_left INT     DEFAULT (0)
    );"""
    cur.execute(sql)

def create_table_student(conn): #cours- 1 = jnr, 2 = snr. Term 1 = 0 
    cur = conn.cursor()
    sql = """CREATE TABLE students (
                id             INTEGER PRIMARY KEY AUTOINCREMENT
                                    UNIQUE
                                    NOT NULL,
                serial      STRING,
                rank        STRING,
                name        STRING  NOT NULL,                
                p_no        STRING,                
                country     STRING,
                gender     STRING,
                grade     STRING,
                specialty     STRING,
                remarks     STRING,
                dept_id     INT     DEFAULT (0),
                course     INT     DEFAULT (0),
                term     INT     DEFAULT NULL,
                group_no     INT     DEFAULT (0),  
                group_triservice_no     INT     DEFAULT (0),                              
                date_created   TEXT
            );"""    
    cur.execute(sql)

def create_table_dept(conn):
    cur = conn.cursor()
    sql = """CREATE TABLE depts (
                id             INTEGER PRIMARY KEY AUTOINCREMENT
                                    UNIQUE
                                    NOT NULL,
                name        STRING  NOT NULL,
                session_id     INT     DEFAULT (0),
                is_deleted     INT     DEFAULT (0),                
                date_created   TEXT
            );"""    
    cur.execute(sql)

def create_table_sessions(conn):
    cur = conn.cursor()
    sql = """CREATE TABLE sessions (
                id             INTEGER         PRIMARY KEY AUTOINCREMENT
                                            UNIQUE
                                            NOT NULL,
                name        STRING          NOT NULL,
                is_current     INT     DEFAULT (0),
                is_deleted      INT               DEFAULT (0),
                date_created TEXT
            );"""
    cur.execute(sql)

def create_table_grouping_dept(conn):
    cur = conn.cursor()
    sql = """CREATE TABLE grouping_dept (
                id             INTEGER         PRIMARY KEY AUTOINCREMENT
                                            UNIQUE
                                            NOT NULL,
                name        STRING,
                dept_id     INT     DEFAULT (0)
            );"""
    cur.execute(sql)

def create_table_grouping_session(conn):
    cur = conn.cursor()
    sql = """CREATE TABLE grouping_session (
                id             INTEGER         PRIMARY KEY AUTOINCREMENT
                                            UNIQUE
                                            NOT NULL,
                name        STRING,
                session_id     INT     DEFAULT (0)
            );"""
    cur.execute(sql)

def create_default_account(conn):
    cur = conn.cursor()
    sql = ''' INSERT INTO account (
                        name,
                        password,
                        trial_left
                    )
                    VALUES (
                        "user",
                        "AFCSC",
                        1
                    ); '''
    cur.execute(sql);
    return 1;

def create_student(conn, data):
    sql = ''' INSERT INTO students(serial,name,rank,p_no,country,gender,grade,specialty,remarks,dept_id,course,term,date_created)
              VALUES(?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, data)
    return cur.lastrowid

def create_agency(conn, data):
    sql = ''' INSERT INTO depts(name,session_id,date_created)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, data)
    return cur.lastrowid

def create_session(conn, data):
    sql = ''' INSERT INTO sessions(name,date_created)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, data)
    return cur.lastrowid

def update_users(conn, data):
    sql = ''' UPDATE users
              SET surname = ? ,
                  firstname = ? ,
                  othername = ? ,
                  biodata = ?,
                  marital_status = ?,
                  dob = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()

def delete_students(conn, dept_id):
    sql = '''DELETE FROM students 
                WHERE dept_id=?'''
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()

def delete_dept(conn, id):
    sql = ''' UPDATE depts
              SET is_deleted = 1
              WHERE id = ?'''
    cur = conn.cursor()
    conn.execute(sql, (id,))
    conn.commit()

def delete_session(conn, id):
    sql = ''' UPDATE sessions
              SET is_deleted = 1
              WHERE id = ?'''
    cur = conn.cursor()
    conn.execute(sql, (id,))
    conn.commit()

def get_students(conn, id):
    sql = "SELECT * FROM students WHERE id = ?"
    cursor = conn.execute(sql, (id,))
    results = cursor.fetchall()
    return results

def get_students_by_agency(conn, dept_id, course, term):
    data = (dept_id, course, term)
    cursor = conn.cursor()
    sql = "SELECT * FROM students WHERE dept_id = ? AND course = ? AND term = ? ORDER BY group_no, name"
    cursor = conn.execute(sql, data)
    results = cursor.fetchall()
    return results

def get_students_by_session(conn, session_id, course, term):
    data = (course, term, session_id)
    cursor = conn.cursor()
    sql = """SELECT * FROM students 
            WHERE course = ? AND term = ?
                AND dept_id IN (
                        SELECT id FROM depts 
                        WHERE is_deleted = 0 AND session_id = ?
                    ) ORDER BY group_triservice_no, dept_id, name"""
    cursor = conn.execute(sql, data)
    results = cursor.fetchall()
    return results

def get_account(conn):
    sql = "SELECT * FROM account"
    results = conn.execute(sql)
    return results

def get_sessions(conn):
    cursor = conn.cursor()
    sql = "SELECT * FROM sessions WHERE is_deleted = 0"
    cursor = conn.execute(sql)
    results = cursor.fetchall()
    return results

def get_sessions_current(conn):
    id = 0
    name = ''

    cursor = conn.cursor()
    sql = "SELECT id, name FROM sessions WHERE is_deleted = 0 AND is_current = 1"
    cursor = conn.execute(sql)
    results = cursor.fetchall()

    if(results):
        for d in results:
            id = d[0]
            name = d[1]
     
    return id,name

def get_agency(conn, session_id):
    cursor = conn.cursor()
    data = (0,session_id)
    sql = "SELECT * FROM depts WHERE is_deleted = ? AND session_id = ?"
    cursor = conn.execute(sql, data)
    results = cursor.fetchall()
    return results

def get_students_by_name(conn, name):    
    cursor = conn.cursor()
    if(not name):
        sql = "SELECT * FROM students"
        cursor.execute(sql)
    else:
        param = (name,name,name)
        sql = "SELECT * FROM students WHERE name LIKE ?"
        cursor.execute(sql, param)
    results = cursor.fetchall()
    return results

def update_student(conn, data):
    sql = ''' UPDATE students
              SET  rank = ?, 
                name = ?, 
                p_no = ?, 
                country = ?, 
                gender = ?, 
                grade = ?, 
                specialty = ?, 
                remarks = ?,
                group_no = ?, 
                group_triservice_no = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()

def update_account(conn, password):
    data = (password, 'user')
    sql = ''' UPDATE account
              SET password = ? ,
                  name = ?
              WHERE id = 1'''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()

def update_account_change_user(conn, user_type):
    data = (user_type, 1)
    sql = ''' UPDATE account
              SET name = ?, trial_left = 0
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()

def update_trial_reduce(conn):
    sql = ''' UPDATE account
              SET trial_left = trial_left-1
              WHERE id = 1'''
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def update_session_current(conn, id = 0, type = 1):
    data = (type, id)
    cur = conn.cursor()

    if(type == 0):
        sql = ''' UPDATE sessions
                SET is_current = 0'''
        cur.execute(sql)
        conn.commit()

    else:
        sql = ''' UPDATE sessions
                SET is_current = ?
                WHERE id = ?'''
        
        cur.execute(sql, data)
        conn.commit()
