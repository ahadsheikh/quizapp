from core.database.database_tools import DBModel

APP_NAME = "quizapp"

class User(DBModel):
    """
        Fields... 
        id, username, password, name, user_type
    """
    table_name = f"{APP_NAME}_users"
    fields = [
        ('id', True),
        ('username', True),
        ('password', True), 
        ('name', True), 
        ('user_type', False)
    ]

class Teacher(DBModel):
    """
        Fields... 
        id, user_id, profile_pic, dept_name, status
    """
    table_name = f"{APP_NAME}_teachers"
    fields = [
        ('id', True), 
        ('user_id', True), 
        ('profile_pic', False), 
        ('dept_name', False), 
        ('status', False)
    ]


class Student(DBModel):
    """
        Fields... 
        id, user_id, profile_pic, age
    """
    table_name = f"{APP_NAME}_students"
    fields = [
        ('id', True), 
        ('user_id', True), 
        ('profile_pic', False), 
        ('age', False)
    ]


class Subject(DBModel):

    """
        Fields... 
        id, subject_name
    """
    table_name = f"{APP_NAME}_subjects"
    fields = [
        ('id', True), 
        ('subject_name', True)
    ]

class Exam(DBModel):
    """
        Fields... 
        id, subject_id(one_to_many), teacher_id, question_id(one_to_many), total_marks
    """
    table_name = f"{APP_NAME}_exams"
    fields = [
        ('id', True), 
        ('subject_id', True), 
        ('teacher_id', True), 
        ('question_id', False), 
        ('total_marks', False)
    ]

class Question(DBModel):
    """
        Fields...
        id, name, mark, opt1, opt2, opt3, opt4, answer
    """
    table_name = f"{APP_NAME}_questions"
    fields = [
        ('id', True), 
        ('name', True),
        ('mark', True), 
        ('opt1', True), 
        ('opt2', True),
        ('opt3', True), 
        ('opt4', True), 
        ('answer', True)
    ]

class Result(DBModel):
    """
        Fields... 
        id, student_id, exam_id, marks
    """
    table_name = f"{APP_NAME}_results"
    fields = [
        ('id', True), 
        ('student_id', True), 
        ('exam_id', True), 
        ('marks', True)
    ]

