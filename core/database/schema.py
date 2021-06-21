from django.conf import settings

import cx_Oracle


APP_NAME = "quizapp"

SQLS = [
    [
        'users', 
        f"""
        CREATE TABLE {APP_NAME}_users (
            id NUMBER(10) NOT NULL PRIMARY KEY,
            username VARCHAR2(20) NOT NULL,
            password VARCHAR2(50) NOT NULL,
            name VARCHAR2(30) NOT NULL, 
            user_type NUMBER DEFAULT 2
        ) 
        """
    ],
    [
        'teachers', 
        f"""
        CREATE TABLE {APP_NAME}_teachers (
            id NUMBER(10) NOT NULL PRIMARY KEY,
            user_id NUMBER(10) NOT NULL,
            profile_pic VARCHAR2(200),
            dept_name VARCHAR2(50), 
            status VARCHAR2(50),
            FOREIGN KEY(user_id) REFERENCES {APP_NAME}_users(id)
        ) 
        """
    ],
    [
        'students', 
        f"""
        CREATE TABLE {APP_NAME}_students (
            id NUMBER(10) NOT NULL PRIMARY KEY,
            user_id NUMBER(10) NOT NULL,
            profile_pic VARCHAR2(200),
            age NUMBER,
            FOREIGN KEY(user_id) REFERENCES {APP_NAME}_users(id)
        ) 
        """
    ],
    [
        'subjects', 
        f"""
        CREATE TABLE {APP_NAME}_subjects (
            id NUMBER(10) NOT NULL PRIMARY KEY,
            subject_name VARCHAR2(100)  
        ) 
        """
    ],
    [
        'questions', 
        f"""
        CREATE TABLE {APP_NAME}_questions (
            id NUMBER(10) NOT NULL PRIMARY KEY,
            name VARCHAR2(256) NOT NULL, 
            mark NUMBER NOT NULL, 
            opt1 VARCHAR2(50) NOT NULL, 
            opt2 VARCHAR2(50) NOT NULL, 
            opt3 VARCHAR2(50) NOT NULL, 
            opt4 VARCHAR2(50) NOT NULL, 
            answer NUMBER NOT NULL
        ) 
        """
    ],
    [
        'exams', 
        f"""
        CREATE TABLE {APP_NAME}_exams (
            id NUMBER(10) NOT NULL PRIMARY KEY,
            subject_id NUMBER NOT NULL,
            teacher_id NUMBER NOT NULL,
            question_id NUMBER,
            total_marks NUMBER,
            FOREIGN KEY(subject_id) REFERENCES {APP_NAME}_subjects(id),
            FOREIGN KEY(teacher_id) REFERENCES {APP_NAME}_teachers(id),
            FOREIGN KEY(question_id) REFERENCES {APP_NAME}_questions(id)
        ) 
        """
    ],
    [
        'results', 
        f"""
        CREATE TABLE {APP_NAME}_results (
            id NUMBER(10) NOT NULL PRIMARY KEY,
            student_id NUMBER NOT NULL, 
            exam_id NUMBER NOT NULL, 
            marks NUMBER NOT NULL, 
            FOREIGN KEY(student_id) REFERENCES {APP_NAME}_students(id),
            FOREIGN KEY(exam_id) REFERENCES {APP_NAME}_exams(id)
        ) 
        """
    ]
    
]

def schemaCreation():
    try:
        connection = cx_Oracle.connect(
            user=settings.CUSTOM_DB_CONFIG['user'],
            password=settings.CUSTOM_DB_CONFIG['password'],
            dsn=settings.CUSTOM_DB_CONFIG['dsn']
        )
        cursor = connection.cursor()
        for table in SQLS:
            try:
                print(f"Creating {table[0]}...")
                cursor.execute(table[1])
            except cx_Oracle.Error as err:
                error, = err.args
                if err == 955:
                    continue
                
    except cx_Oracle.Error as err:
        error, = err.args
        print("Oracle-Error-Code:", error.code)
        print("Oracle-Error-Message:", error.message)
