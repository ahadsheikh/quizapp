from django import forms
from django.contrib.auth.models import User
from django.forms import fields
from . import models

class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

class TeacherSalaryForm(forms.Form):
    salary=forms.IntegerField()

class CourseForm(forms.ModelForm):
    class Meta:
        model=models.Course
        fields=['course_name']

class QuestionForm(forms.ModelForm):
    class Meta:
        model=models.Question
        fields=['question','mark', 'option1','option2','option3','option4', 'answer']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50})
        }

class ExamForm(forms.ModelForm):
    class Meta:
        model = models.Exam
        fields = ['subject', 'question', 'marks']