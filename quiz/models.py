from django.db import models

from teacher.models import Teacher
from student.models import Student
class Course(models.Model):
   course_name = models.CharField(max_length=50)
   def __str__(self):
        return self.course_name

class Question(models.Model):
    cat=((1, 'Option1'),(1, 'Option2'),(3, 'Option3'),(4, 'Option4'))

    question=models.CharField(max_length=600)
    mark=models.PositiveIntegerField()
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)
    answer=models.IntegerField(choices=cat)

    def __str__(self):
        return self.question

class Exam(models.Model):
    subject = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    question = models.ManyToManyField(Question, blank=True)
    marks = models.IntegerField(blank=True)

    def __str__(self):
        return self.subject.course_name

class Result(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    marks = models.IntegerField()

    def __str__(self):
        return self.student.user.username + "'s results"