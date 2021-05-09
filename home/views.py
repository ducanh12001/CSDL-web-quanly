from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .models import Teachers, CourseList, Students, StudentResult
from django.contrib import messages


def home_page(request):
    if request.user.is_authenticated:
        return render(request, 'home_log.html')
    else:
        return render(request, 'home.html')


@login_required(login_url='home:login')
def home_log_page(request):
    if request.user.is_authenticated:
        return render(request, 'home_log.html')
    else:
        redirect('home:login')


def search_page(request):
    return render(request, 'search.html')


class ManagePage(View):
    def get(self, request):
        return render(request, 'manage.html')


class AddStudentPage(View):
    def get(self, request):
        return render(request, 'addStudent.html')


class LoginUser(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user = request.POST['userName']
        user_pass = request.POST['userPassword']
        this_user = authenticate(username=user, password=user_pass)

        if this_user is not None:
            login(request, this_user)
            return redirect('home:home_log')
        else:
            messages.info(request, 'Username or Password is incorrect!')

        context = {}
        return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    return redirect('home:home_page')


def cmp_by_course_id(element):
    return element.courseID


class SearchClass(View):
    def get(self, request):
        course_data = CourseList.objects.all().order_by('courseID')
        return render(request, 'searchClass.html', {'courseData': course_data})

    def post(self, request):
        user_search = request.POST['searchClass']
        course_data_by_id = CourseList.objects.filter(courseID__icontains=user_search)
        course_data_by_name = CourseList.objects.filter(courseName__icontains=user_search)
        data_list = []

        for c in course_data_by_name:
            data_list.append(c)
        for c in course_data_by_id:
            data_list.append(c)

        data_list.sort(key=cmp_by_course_id)

        if len(data_list) > 1:
            new_list = [data_list[0]]

            for i in range(1, len(data_list)):
                if data_list[i].courseID != data_list[i - 1].courseID:
                    new_list.append(data_list[i])

        return render(request, "searchClass.html", {'courseData': new_list})


def cmp_by_student_id(element):
    return element.studentID


class SearchStudent(View):
    def get(self, request):
        students_data = Students.objects.all().order_by("studentName")
        return render(request, 'searchStudent.html', {'studentData': students_data})

    def post(self, request):
        user_search = request.POST['searchStudent']
        student_by_id = Students.objects.filter(studentID__icontains=user_search)
        student_by_name = Students.objects.filter(studentName__icontains=user_search)

        data_list = []

        for s in student_by_id:
            data_list.append(s)
        for s in student_by_name:
            data_list.append(s)

        data_list.sort(key=cmp_by_student_id)

        if len(data_list) > 1:
            new_list = [data_list[0]]

            for i in range(1, len(data_list)):
                if data_list[i].studentID != data_list[i - 1].studentID:
                    new_list.append(data_list[i])
                elif data_list[i].belongToCourse.courseID != data_list[i - 1].belongToCourse.courseID:
                    new_list.append(data_list[i])

        return render(request, "searchStudent.html", {'studentData': new_list})


class SearchTeacher(View):
    def get(self, request):
        return render(request, 'searchTeacher.html')
