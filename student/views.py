from django.http.response import HttpResponse
from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from quiz import models as QMODEL

from teacher import models as TMODEL
from core.database.models import Result, User as OracleUser, Student


#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'student/studentclick.html')

def student_signup_view(request):
    userForm=forms.StudentUserForm()
    studentForm=forms.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.StudentUserForm(request.POST)
        studentForm=forms.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

            # Saving User Data in Oracle Database
            userObj = OracleUser()
            userObjData = {
                'id': user.id,
                'username': user.username,
                'password': request.POST['password'],
                'name': user.first_name + user.last_name,
            }
            # Saving Student Data in Oracle Database
            studentObj = Student()
            studentObjData = {
                'id': student.id,
                'user_id': user.id,
                'profile_pic': student.profile_pic.path
            }

            userObj.create(userObjData)
            studentObj.create(studentObjData)
            userObj.close()
            studentObj.close()
            
        return HttpResponseRedirect('studentlogin')
    return render(request,'student/studentsignup.html',context=mydict)

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    dict={
    
    'total_course':QMODEL.Course.objects.all().count(),
    'total_question':QMODEL.Question.objects.all().count(),
    }
    return render(request,'student/student_dashboard.html',context=dict)

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_exam_view(request):
    exams=QMODEL.Exam.objects.all()
    return render(request,'student/student_exam.html',{'exams':exams})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def take_exam_view(request,pk):
    exam=QMODEL.Exam.objects.get(id=pk)
    total_questions = len(exam.question.all())
    questions = exam.question.all()
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.mark
    
    return render(request,'student/take_exam.html',{'exam': exam,'total_questions':total_questions,'total_marks':total_marks})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def start_exam_view(request,pk):
    exam = QMODEL.Exam.objects.get(id=pk)
    questions = questions = exam.question.all()
    if request.method=='POST':
        pass
    response= render(request,'student/start_exam.html',{'exam': exam, 'questions': questions})
    response.set_cookie('exam_id',exam.id)
    return response


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def calculate_marks_view(request):
    print(request.COOKIES)
    if request.COOKIES.get('exam_id') is not None:
        exam_id = request.COOKIES.get('exam_id')
        exam = QMODEL.Exam.objects.get(id=exam_id)
        
        total_marks=0
        questions = exam.question.all()
        i = 0
        for q in questions:
            selected_ans = request.COOKIES.get(str(i+1))[-1]
            print(selected_ans, q.answer)
            actual_answer = q.answer
            if int(selected_ans) == int(actual_answer):
                total_marks = total_marks + q.mark

        student = request.user.student
        result = QMODEL.Result()
        result.marks = total_marks
        result.exam = exam
        result.student = student
        print(total_marks, result)
        result.save()

        resultObj = Result()
        resultObj.create(
            {
                'id': result.id,
                'student_id': student.id,
                'exam_id': exam.id,
                'marks': total_marks
            }
        )
        resultObj.close()

        return HttpResponseRedirect('view-result')



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def view_result_view(request):
    exams=QMODEL.Exam.objects.all()
    return render(request,'student/view_result.html',{'exams':exams})
    

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def check_marks_view(request,pk):
    course=QMODEL.Exam.objects.get(id=pk)
    student = models.Student.objects.get(user_id=request.user.id)
    results= QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'student/check_marks.html',{'results':results})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_marks_view(request):
    student = request.user.student
    results = QMODEL.Result.objects.filter(student=student)
    res = []
    for r in results:
        res.append({
            'subject': r.exam.subject.course_name,
            'marks': r.marks
        })
    return render(request,'student/student_marks.html',{'results':res})
  