
-- quiz_users table queries
-- table creation
CREATE TABLE quiz_users (
    id NUMBER(10) NOT NULL PRIMARY KEY,
    username VARCHAR2(20) NOT NULL,
    password VARCHAR2(50) NOT NULL,
    name VARCHAR2(30) NOT NULL, 
    user_type NUMBER DEFAULT 2 
);
-- get table data
SELECT * FROM quiz_users;
-- insert data
INSERT INTO quiz_users VALUES(2, 'kabir', '1234', 'Kabir Mahmud', 2);
-- update data
UPDATE quiz_users
SET name = 'Kabir',
    user_type = 2
WHERE id = 3;
-- delete data
DELETE FROM quiz_users 
WHERE id = 2


-- quiz_teachers table queries
-- table creation
CREATE TABLE quiz_teachers (
    id NUMBER(10) NOT NULL PRIMARY KEY,
    user_id NUMBER(10) NOT NULL,
    profile_pic VARCHAR2(200),
    dept_name VARCHAR2(50), 
    status VARCHAR2(50),
    FOREIGN KEY(user_id) REFERENCES quiz_users(id)
);
-- get table data
SELECT * FROM quiz_teachers;
-- insert data
INSERT INTO quiz_teachers VALUES(2, 1, 'profile_pic path', 'cse', 'Professor');
-- update data
UPDATE quiz_teachers
SET dept_name = 'eee'
WHERE id = 3;
-- delete data
DELETE FROM quiz_teachers
WHERE id = 2


-- quiz_students table queries
-- table creation
CREATE TABLE quiz_students (
    id NUMBER(10) NOT NULL PRIMARY KEY,
    user_id NUMBER(10) NOT NULL,
    profile_pic VARCHAR2(200),
    age NUMBER,
    FOREIGN KEY(user_id) REFERENCES quiz_users(id)
)
-- get table data
SELECT * FROM quiz_students;
-- insert data
INSERT INTO quiz_students VALUES(2, 1, 'profile pic path', 23);
-- update data
UPDATE quiz_students
SET age = 28
WHERE id = 3;
-- delete data
DELETE FROM quiz_students 
WHERE id = 2


-- quiz_subjects table queries
-- table creation
CREATE TABLE quiz_subjects (
    id NUMBER(10) NOT NULL PRIMARY KEY,
    subject_name VARCHAR2(100) 
)
-- get table data
SELECT * FROM quiz_subjects;
-- insert data
INSERT INTO quiz_subjects VALUES(2, 'eee');
-- update data
UPDATE quiz_subjects
SET subject_name = 'cse'
WHERE id = 3;
-- delete data
DELETE FROM quiz_subjects 
WHERE id = 2



-- quiz_questions table queries
-- table creation
CREATE TABLE quiz_questions (
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
SELECT * FROM quiz_questions;
-- insert data
INSERT INTO quiz_questions 
VALUES(2, 'Whats the capital of Bangladesh', 1, 'Dhaka', 'Delhi', 'London', 'Tokyo', 1);
-- update data
UPDATE quiz_questions
SET name = 'Whats the capital of Bangladesh'
WHERE id = 3;
-- delete data
DELETE FROM quiz_questions 
WHERE id = 2


-- quiz_exams table queries
-- table creation
CREATE TABLE quiz_exams (
    id NUMBER(10) NOT NULL PRIMARY KEY,
    subject_id NUMBER NOT NULL,
    teacher_id NUMBER NOT NULL,
    question_id NUMBER,
    total_marks NUMBER,
    FOREIGN KEY(subject_id) REFERENCES quiz_subjects(id),
    FOREIGN KEY(teacher_id) REFERENCES quiz_teachers(id),
    FOREIGN KEY(question_id) REFERENCES quiz_questions(id)
)
-- get table data
SELECT * FROM quiz_exams;
-- insert data
INSERT INTO quiz_exams VALUES(2, 1, 2, 3, 1);
-- update data
UPDATE quiz_exams
SET total_marks = 3
WHERE id = 3;
-- delete data
DELETE FROM quiz_exams 
WHERE id = 2


-- quiz_results table queries
-- table creation
CREATE TABLE quiz_results (
    id NUMBER(10) NOT NULL PRIMARY KEY,
    student_id NUMBER NOT NULL, 
    exam_id NUMBER NOT NULL, 
    marks NUMBER NOT NULL, 
    FOREIGN KEY(student_id) REFERENCES quiz_students(id),
    FOREIGN KEY(exam_id) REFERENCES quiz_exams(id)
)
-- get table data
SELECT * FROM quiz_results;
-- insert data
INSERT INTO quiz_results VALUES(2, 3, 4, 2);
-- update data
UPDATE quiz_results
SET marks = 30
WHERE id = 3;
-- delete data
DELETE FROM quiz_results 
WHERE id = 2