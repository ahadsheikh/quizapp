from django.shortcuts import render, redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from teacher import models as TMODEL
from student import models as SMODEL
from quiz import models as QMODEL
from teacher import forms as TFORM
from student import forms as SFORM
from django.contrib.auth.models import User

from core.database.models import Question, Result, User as OracleUser, Teacher, Student, Exam, Subject


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    return render(request,'quiz/index.html')


def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def afterlogin_view(request):
    if is_student(request.user):      
        return redirect('student/student-dashboard')
                
    elif is_teacher(request.user):
        return redirect('teacher/teacher-dashboard')
    else:
        return redirect('admin-dashboard')



def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    'total_teacher':TMODEL.Teacher.objects.all().count(),
    'total_course':models.Course.objects.all().count(),
    'total_question':models.Question.objects.all().count(),
    }
    return render(request,'quiz/admin_dashboard.html',context=dict)

@login_required(login_url='adminlogin')
def admin_teacher_view(request):
    dict={
        'total_teacher':TMODEL.Teacher.objects.all().count(),
    }
    print(dict)
    return render(request,'quiz/admin_teacher.html',context=dict)

@login_required(login_url='adminlogin')
def admin_view_teacher_view(request):
    teachers= TMODEL.Teacher.objects.all()
    return render(request,'quiz/admin_view_teacher.html',{'teachers':teachers})


@login_required(login_url='adminlogin')
def update_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=TMODEL.User.objects.get(id=teacher.user_id)
    userForm=TFORM.TeacherUserUpdateForm(instance=user)
    teacherForm=TFORM.TeacherForm(request.FILES,instance=teacher)
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    if request.method=='POST':
        userForm=TFORM.TeacherUserUpdateForm(request.POST,instance=user)
        teacherForm=TFORM.TeacherForm(request.POST,request.FILES,instance=teacher)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            teacher=teacherForm.save()

            # Saving User Data in Oracle Database
            userObj = OracleUser()
            userObjData = {
                'username': user.username,
                'name': user.first_name +  " " +user.last_name,
            }
            # Saving Student Data in Oracle Database
            teacherObj = Teacher()
            teacherObjData = {
                'profile_pic': teacher.profile_pic.path,
                'dept_name': teacher.dept_name,
                'status': teacher.status
            }
            print(userObjData, teacherObjData)
            userObj.update_by_id(user.id, userObjData)
            
            sql = f"select id from quizapp_teachers where user_id = {user.id}"
            teacher_id = teacherObj.execute_select_sql(sql)
            teacherObj.update_by_id(teacher_id[0]['id'], teacherObjData)
            userObj.close()
            teacherObj.close()

            return redirect('admin-view-teacher')
    return render(request,'quiz/update_teacher.html', context=mydict)



@login_required(login_url='adminlogin')
def delete_teacher_view(request,pk):
    teacher = TMODEL.Teacher.objects.get(id=pk)
    user = teacher.user
    user.id = user.id
    
    # Saving User Data in Oracle Database
    userObj = OracleUser()

    teacherObj = Teacher()
    sql = f"select id from quizapp_teachers where user_id = {user.id}"
    teacher_id = teacherObj.execute_select_sql(sql)
    print(teacher_id)
    

    examObj = Exam()
    sql = f"select id from quizapp_exams where teacher_id = {teacher_id}"
    exam_id = examObj.execute_select_sql(sql)
    print(exam_id)

    print(teacher_id, exam_id)

    if exam_id is not None:
        exam_id = exam_id[0]['id']
        examObj.delete_by_id(exam_id)
    if teacher_id is not None:
        teacher_id = teacher_id[0]['id']
        teacherObj.delete_by_id(teacher_id)

    examObj.close()
    teacherObj.close()
        

    # Delete Oracle Database data
    userObj.delete_by_id(user.id)
    userObj.close()

    # Delete Django User
    user.delete()
    
    return HttpResponseRedirect('/admin-view-teacher')




@login_required(login_url='adminlogin')
def admin_view_pending_teacher_view(request):
    teachers= TMODEL.Teacher.objects.all()
    return render(request,'quiz/admin_view_pending_teacher.html',{'teachers':teachers})


@login_required(login_url='adminlogin')
def approve_teacher_view(request,pk):
    teacherSalary=forms.TeacherSalaryForm()
    if request.method=='POST':
        teacherSalary=forms.TeacherSalaryForm(request.POST)
        if teacherSalary.is_valid():
            teacher=TMODEL.Teacher.objects.get(id=pk)
            teacher.salary=teacherSalary.cleaned_data['salary']
            teacher.status=True
            teacher.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-pending-teacher')
    return render(request,'quiz/salary_form.html',{'teacherSalary':teacherSalary})

@login_required(login_url='adminlogin')
def reject_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    
    
    

    return HttpResponseRedirect('/admin-view-pending-teacher')



@login_required(login_url='adminlogin')
def admin_view_teacher_salary_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=True)
    return render(request,'quiz/admin_view_teacher_salary.html',{'teachers':teachers})


    




@login_required(login_url='adminlogin')
def admin_student_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    }
    return render(request,'quiz/admin_student.html',context=dict)

@login_required(login_url='adminlogin')
def admin_view_student_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'quiz/admin_view_student.html',{'students':students})



@login_required(login_url='adminlogin')
def update_student_view(request,pk):
    student = SMODEL.Student.objects.get(id=pk)
    user = student.user
    userForm = SFORM.StudentUserUpdateForm(instance=user)
    studentForm = SFORM.StudentForm(request.FILES,instance=student)
    mydict = {'userForm':userForm,'studentForm':studentForm}
    if request.method == 'POST':
        userForm=SFORM.StudentUserUpdateForm(request.POST,instance=user)
        studentForm=SFORM.StudentForm(request.POST,request.FILES,instance=student)
        if userForm.is_valid() and studentForm.is_valid():
            user = userForm.save()
            user.save()
            student = studentForm.save()

            # Saving User Data in Oracle Database
            userObj = OracleUser()
            userObjData = {
                'username': user.username,
                'name': user.first_name + " " +user.last_name,
            }
            # Saving Student Data in Oracle Database
            studentObj = Student()
            studentObjData = {
                'profile_pic': student.profile_pic.path,
                'age': student.age,
            }
            print(userObjData, studentObjData)
            userObj.update_by_id(user.id, userObjData)
            
            sql = f"select id from quizapp_students where user_id = {user.id}"
            student_id = studentObj.execute_select_sql(sql)
            studentObj.update_by_id(student_id[0]['id'], studentObjData)
            userObj.close()
            studentObj.close()

            return redirect('admin-view-student')
    return render(request,'quiz/update_student.html',context=mydict)



@login_required(login_url='adminlogin')
def delete_student_view(request, pk):
    student = SMODEL.Student.objects.get(id=pk)
    user = student.user

    # Saving User Data in Oracle Database
    userObj = OracleUser()

    studentObj = Student()
    sql = f"select id from quizapp_students where user_id = {user.id}"
    student_id = studentObj.execute_select_sql(sql)

    resultObj = Result()
    sql = f"select id from quizapp_results where student_id = {student_id}"
    result_id = resultObj.execute_select_sql(sql)

    print(student_id, result_id)

    if result_id is not None:
        result_id = result_id[0]['id']
        resultObj.delete_by_id(result_id)
    if student_id is not None:
        student_id = student_id[0]['id']
        studentObj.delete_by_id(student_id)

    resultObj.close()
    studentObj.close()
        

    # Delete Oracle Database data
    userObj.delete_by_id(user.id)
    userObj.close()

    # Delete Django User
    user.delete()

    return HttpResponseRedirect('/admin-view-student')


@login_required(login_url='adminlogin')
def admin_course_view(request):
    return render(request,'quiz/admin_course.html')


@login_required(login_url='adminlogin')
def admin_add_course_view(request):
    courseForm=forms.CourseForm()
    if request.method=='POST':
        courseForm=forms.CourseForm(request.POST)
        if courseForm.is_valid():    
            sub = courseForm.save()
            subObj = Subject()
            subObj.create({
                'id': sub.id,
                'subject_name': sub.course_name
            })
            subObj.close()

            return HttpResponseRedirect('/admin-view-course')

        else:
            print("form is invalid")
        
    return render(request,'quiz/admin_add_course.html',{'courseForm':courseForm})


@login_required(login_url='adminlogin')
def admin_view_course_view(request):
    courses = models.Course.objects.all()
    return render(request,'quiz/admin_view_course.html',{'courses':courses})

@login_required(login_url='adminlogin')
def delete_course_view(request,pk):
    course = models.Course.objects.get(id=pk)

    subObj = Subject()
    subObj.delete_by_id(course.id)
    subObj.close()

    course.delete()
    return HttpResponseRedirect('/admin-view-course')



@login_required(login_url='adminlogin')
def admin_question_view(request):
    return render(request,'quiz/admin_question.html')


@login_required(login_url='adminlogin')
def admin_add_question_view(request):
    questionForm=forms.QuestionForm()
    if request.method=='POST':
        questionForm=forms.QuestionForm(request.POST)
        if questionForm.is_valid():
            question=questionForm.save()
            question.save()  

            # Oracle data creation
            quesObj = Question()
            quesObj.create(
                {
                    'id': question.id,
                    'name': question.question,
                    'mark': question.mark,
                    'opt1': question.option1,
                    'opt2': question.option2,
                    'opt3': question.option3,
                    'opt4': question.option4,
                    'answer': question.answer
                }
            )
            quesObj.close()
                 
            return HttpResponseRedirect('/admin-view-question')
        else:
            print("form is invalid")
        
    return render(request,'quiz/admin_add_question.html',{'questionForm':questionForm})


@login_required(login_url='adminlogin')
def admin_view_question_view(request):
    questions = models.Question.objects.all()
    return render(request,'quiz/admin_view_question.html',{'questions': questions})

@login_required(login_url='adminlogin')
def view_question_view(request,pk):
    question = models.Question.objects.get(id=pk)
    return render(request,'quiz/view_question.html',{'question':question})

@login_required(login_url='adminlogin')
def delete_question_view(request,pk):
    question=models.Question.objects.get(id=pk)

    # Remove from oracle
    questionObj = Question()
    questionObj.delete_by_id(pk)
    questionObj.close()

    question.delete()
    return HttpResponseRedirect('/admin-view-question')

@login_required(login_url='adminlogin')
def admin_view_student_marks_view(request):
    results= QMODEL.Result.objects.all()
    return render(request,'quiz/admin_view_student_marks.html',{'results':results})



@login_required(login_url='adminlogin')
def admin_view_marks_view(request,pk):
    courses = models.Course.objects.all()
    response =  render(request,'quiz/admin_view_marks.html',{'courses':courses})
    response.set_cookie('student_id',str(pk))
    return response

@login_required(login_url='adminlogin')
def admin_check_marks_view(request,pk):
    course = models.Course.objects.get(id=pk)
    student_id = request.COOKIES.get('student_id')
    student= SMODEL.Student.objects.get(id=student_id)

    results= models.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'quiz/admin_check_marks.html',{'results':results})


def aboutus_view(request):
    return render(request,'quiz/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'quiz/contactussuccess.html')
    return render(request, 'quiz/contactus.html', {'form':sub})


