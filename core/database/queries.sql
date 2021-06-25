
-- quizapp_users table queries
-- table creation
CREATE TABLE quizapp_users (
    id NUMBER(10) NOT NULL PRIMARY KEY,
    username VARCHAR2(20) NOT NULL,
    password VARCHAR2(50) NOT NULL,
    name VARCHAR2(30) NOT NULL, 
    user_type NUMBER DEFAULT 2 
);
-- get table data
SELECT * FROM quizapp_users;
-- insert data
INSERT INTO quizapp_users VALUES(2, 'kabir', '1234', 'Kabir Mahmud', 2);
-- update data
UPDATE quizapp_users
SET name = 'Kabir',
    user_type = 2
WHERE id = 3;
-- delete data
DELETE FROM quizapp_users 
WHERE id = 2


-- quizapp_teachers table queries
-- table creation
CREATE TABLE quizapp_teachers (
    id NUMBER(10) NOT NULL PRIMARY KEY,
    user_id NUMBER(10) NOT NULL,
    profile_pic VARCHAR2(200),
    dept_name VARCHAR2(50), 
    status VARCHAR2(50),
    FOREIGN KEY(user_id) REFERENCES quizapp_users(id)
);
-- get table data
SELECT * FROM quizapp_teachers;
-- insert data
INSERT INTO quizapp_teachers VALUES(2, 1, 'profile_pic path', 'cse', 'Professor');
-- update data
UPDATE quizapp_teachers
SET dept_name = 'eee'
WHERE id = 3;
-- delete data
DELETE FROM quizapp_teachers
WHERE id = 2


-- quizapp_students table queries
-- table creation
CREATE TABLE quizapp_students (
    id NUMBER(10) NOT NULL PRIMARY KEY,
    user_id NUMBER(10) NOT NULL,
    profile_pic VARCHAR2(200),
    age NUMBER,
    FOREIGN KEY(user_id) REFERENCES quizapp_users(id)
)
-- get table data
SELECT * FROM quizapp_students;
-- insert data
INSERT INTO quizapp_students VALUES(2, 1, 'profile pic path', 23);
-- update data
UPDATE quizapp_students
SET age = 28
WHERE id = 3;
-- delete data
DELETE FROM quizapp_students 
WHERE id = 2


-- quizapp_subjects table queries
-- table creation
CREATE TABLE quizapp_subjects (
    id NUMBER(10) NOT NULL PRIMARY KEY,
    subject_name VARCHAR2(100) 
)
-- get table data
SELECT * FROM quizapp_subjects;
-- insert data
INSERT INTO quizapp_subjects VALUES(2, 'eee');
-- update data
UPDATE quizapp_subjects
SET subject_name = 'cse'
WHERE id = 3;
-- delete data
DELETE FROM quizapp_subjects 
WHERE id = 2



-- quizapp_questions table queries
-- table creation
CREATE TABLE quizapp_questions (
    id NUMBER(10) NOT NULL PRIMARY KEY,
    name VARCHAR2(256) NOT NULL, 
    mark NUMBER NOT NULL, 
    opt1 VARCHAR2(50) NOT NULL, 
    opt2 VARCHAR2(50) NOT NULL, 
    opt3 VARCHAR2(50) NOT NULL, 
    opt4 VARCHAR2(50) NOT NULL, 
    answer NUMBER NOT NULL
)
-- get table data
SELECT * FROM quizapp_questions;
-- insert data
INSERT INTO quizapp_questions 
VALUES(2, 'Whats the capital of Bangladesh', 1, 'Dhaka', 'Delhi', 'London', 'Tokyo', 1);
-- update data
UPDATE quizapp_questions
SET name = 'Whats the capital of Bangladesh'
WHERE id = 3;
-- delete data
DELETE FROM quizapp_questions 
WHERE id = 2


-- quizapp_exams table queries
-- table creation
CREATE TABLE quizapp_exams (
    id NUMBER(10) NOT NULL PRIMARY KEY,
    subject_id NUMBER NOT NULL,
    teacher_id NUMBER NOT NULL,
    question_id NUMBER,
    total_marks NUMBER,
    FOREIGN KEY(subject_id) REFERENCES quizapp_subjects(id),
    FOREIGN KEY(teacher_id) REFERENCES quizapp_teachers(id),
    FOREIGN KEY(question_id) REFERENCES quizapp_questions(id)
)
-- get table data
SELECT * FROM quizapp_exams;
-- insert data
INSERT INTO quizapp_exams VALUES(2, 1, 2, 3, 1);
-- update data
UPDATE quizapp_exams
SET total_marks = 3
WHERE id = 3;
-- delete data
DELETE FROM quizapp_exams 
WHERE id = 2


-- quizapp_results table queries
-- table creation
CREATE TABLE quizapp_results (
    id NUMBER(10) NOT NULL PRIMARY KEY,
    student_id NUMBER NOT NULL, 
    exam_id NUMBER NOT NULL, 
    marks NUMBER NOT NULL, 
    FOREIGN KEY(student_id) REFERENCES quizapp_students(id),
    FOREIGN KEY(exam_id) REFERENCES quizapp_exams(id)
)
-- get table data
SELECT * FROM quizapp_results;
-- insert data
INSERT INTO quizapp_results VALUES(2, 3, 4, 2);
-- update data
UPDATE quizapp_results
SET marks = 30
WHERE id = 3;
-- delete data
DELETE FROM quizapp_results 
WHERE id = 2


-- Users table trigger for backup
CREATE OR REPLACE TRIGGER quizapp_users_backup_trigger
BEFORE DELETE ON quizapp_users
FOR EACH ROW
BEGIN
    INSERT INTO quizapp_users_backup 
        (id, username, password, name, user_type, deleted_at)
    values(:OLD.id, :OLD.username, :OLD.password, :OLD.name, :OLD.user_type, CURRENT_TIMESTAMP);
END;
