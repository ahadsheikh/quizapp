from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from quiz import models as QMODEL
from student import models as SMODEL
from quiz import forms as QFORM

from core.database.models import User as OracleUser, Teacher, Subject, Exam, Question


#for showing signup/login button for teacher
def teacherclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'teacher/teacherclick.html')

def teacher_signup_view(request):
    userForm=forms.TeacherUserForm()
    teacherForm=forms.TeacherForm()
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    if request.method=='POST':
        userForm=forms.TeacherUserForm(request.POST)
        teacherForm=forms.TeacherForm(request.POST,request.FILES)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            teacher=teacherForm.save(commit=False)
            teacher.user=user
            teacher.save()
            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)

            # Saving User Data in Oracle Database
            userObj = OracleUser()
            userObjData = {
                'id': user.id,
                'username': user.username,
                'password': request.POST['password'],
                'name': user.first_name + user.last_name,
                'user_type': 1
            }
            # Saving Student Data in Oracle Database
            teacherObj = Teacher()
            teacherObjData = {
                'id': teacher.id,
                'user_id': user.id,
                'profile_pic': teacher.profile_pic.path,
                'dept_name': teacher.dept_name,
                'status': teacher.status
            }
            print(userObjData, teacherObjData)
            userObj.create(userObjData)
            teacherObj.create(teacherObjData)
            userObj.close()
            teacherObj.close()
        return HttpResponseRedirect('teacherlogin')
    return render(request,'teacher/teachersignup.html',context=mydict)



def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    dict={
    
    'total_course':QMODEL.Course.objects.all().count(),
    'total_question':QMODEL.Question.objects.all().count(),
    'total_student':SMODEL.Student.objects.all().count()
    }
    return render(request,'teacher/teacher_dashboard.html',context=dict)

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_exam_view(request):
    return render(request,'teacher/teacher_exam.html')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_exam_view(request):
    courseForm=QFORM.ExamForm()
    if request.method=='POST':
        examForm=QFORM.ExamForm(request.POST)
        if examForm.is_valid():        
            exam = QMODEL.Exam()
            
            print(request.user.teacher)
            exam.subject = examForm.cleaned_data['subject']
            exam.teacher = request.user.teacher
            if examForm.cleaned_data['marks']:
                exam.marks = examForm.cleaned_data['marks']
            else:
                m = 0
                for q in examForm.cleaned_data['question']:
                    m = m + q.mark
                exam.marks = m
                
            exam.save()
            for q in examForm.cleaned_data['question']:
                exam.question.add(q)
            exam.save()

            # Oracle Database 
            examObj = Exam()
            for q in examForm.cleaned_data['question']:
                print(exam.subject.id, request.user.teacher.id, q.id, exam.marks)
                examObj.create({
                    'id': len(examObj.find())+1, 
                    'subject_id': exam.subject.id,
                    'teacher_id': request.user.teacher.id,
                    'question_id': q.id,
                    'total_marks': exam.marks
                })
            examObj.close()
            return HttpResponseRedirect('/teacher/teacher-view-exam')
        else:
            print("form is invalid")

    return render(request,'teacher/teacher_add_exam.html',{'courseForm':courseForm})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_exam_view(request):
    exams = QMODEL.Exam.objects.all()
    mexam = []
    for e in exams:
        mexam.append(
            {
                'id': e.id,
                'subject': e.subject.course_name,
                'teacher': e.teacher.user.first_name + e.teacher.user.last_name,
                'marks': e.marks
            }
        )
    return render(request,'teacher/teacher_view_exam.html', {'exams': mexam})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def delete_exam_view(request, pk):
    exam=QMODEL.Exam.objects.get(id=pk)

    examObj = Exam()
    examObj.delete_by_id(pk)
    examObj.close()

    exam.delete()
    return HttpResponseRedirect('/teacher/teacher-view-exam')

@login_required(login_url='adminlogin')
def teacher_question_view(request):
    return render(request,'teacher/teacher_question.html')

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_question_view(request):
    questionForm=QFORM.QuestionForm()
    if request.method=='POST':
        print(request.POST)
        questionForm=QFORM.QuestionForm(request.POST)
        if questionForm.is_valid():
            question = questionForm.save()

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
            return HttpResponseRedirect('/teacher/teacher-view-question')
        else:
            print("form is invalid")

    return render(request,'teacher/teacher_add_question.html',{'questionForm':questionForm})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_question_view(request):
    questions= QMODEL.Question.objects.all()
    return render(request,'teacher/teacher_view_question.html',{'questions': questions})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def see_question_view(request,pk):
    question=QMODEL.Question.objects.get(id=pk)
    return render(request,'teacher/see_question.html',{'question':question})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def remove_question_view(request,pk):
    question=QMODEL.Question.objects.get(id=pk)

    # Remove from oracle
    questionObj = Question()
    questionObj.delete_by_id(pk)
    questionObj.close()

    question.delete()
    return HttpResponseRedirect('/teacher/teacher-view-question')

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_student_marks_view(request):
    t = request.user
    res= QMODEL.Result.objects.all()
    results = []
    for r in res:
        if r.exam.teacher.user == t:
            results.append(r)
    return render(request,'teacher/teacher_view_student_marks_view.html',{'results':results})