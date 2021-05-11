from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .models import Teachers, CourseList, Students, StudentResult
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
from array import *


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


@login_required(login_url='home:login')
def manage_classes(request):
    teacher_all_courses = request.user.teachers.courselist_set.all().order_by("courseID")

    if request.method == "POST":
        chosen_course_id = request.POST['courseSelected']

        if chosen_course_id == 'Select Class':
            return render(request, 'manage.html', {'teacherAllCourses': teacher_all_courses})

        chosen_course = CourseList.objects.get(courseID=chosen_course_id)

        all_students = chosen_course.students_set.all().order_by("-studentName")

        data_paginator = Paginator(all_students, 10)
        page = request.GET.get('page', 1)
        try:
            page_data = data_paginator.page(page)
        except PageNotAnInteger:
            page_data = data_paginator.page(1)
        except EmptyPage:
            page_data = data_paginator.page(data_paginator.num_pages)

        return render(request, 'manage.html', {'teacherAllCourses': teacher_all_courses, 'allStudents': page_data})
    else:
        return render(request, 'manage.html', {'teacherAllCourses': teacher_all_courses})


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

        for c in course_data:
            c.students_set
            c.studentNumber = c.students_set.count()
            c.save()

        data_paginator = Paginator(course_data, 6)
        page = request.GET.get('page', 1)
        try:
            page_data = data_paginator.page(page)
        except PageNotAnInteger:
            page_data = data_paginator.page(1)
        except EmptyPage:
            page_data = data_paginator.page(data_paginator.num_pages)

        return render(request, 'searchClass.html', {'courseData': page_data})

    def post(self, request):
        user_search = request.POST['searchClass']
        course_data_by_id = CourseList.objects.filter(courseID__icontains=user_search)
        course_data_by_name = CourseList.objects.filter(courseName__icontains=user_search)

        data_list = []
        for c in course_data_by_id:
            data_list.append(c)
        for c in course_data_by_name:
            data_list.append(c)

        if len(data_list) > 0:
            data_list.sort(key=cmp_by_course_id)
            new_list = [data_list[0]]

            for i in range(1, len(data_list)):
                if data_list[i].courseID != data_list[i - 1].courseID:
                    new_list.append(data_list[i])

        data_paginator = Paginator(new_list, 6)
        page = request.GET.get('page', 1)
        try:
            page_data = data_paginator.page(page)
        except PageNotAnInteger:
            page_data = data_paginator.page(1)
        except EmptyPage:
            page_data = data_paginator.page(data_paginator.num_pages)

        return render(request, 'searchClass.html', {'courseData': page_data})


def cmp_by_student_id(element):
    return element.studentID


class SearchStudent(View):
    def get(self, request):
        all_students = Students.objects.all().order_by("-studentID")
        last_data = []  # Cái này là cái danh sách cuối

        if len(all_students) > 0:
            for student in all_students:
                courses = student.belongToCourse.all()
                for course in courses:
                    last_data.append({'student': student, 'course': course})

        data_paginator = Paginator(last_data, 6)
        page = request.GET.get('page', 1)
        try:
            page_data = data_paginator.page(page)
        except PageNotAnInteger:
            page_data = data_paginator.page(1)
        except EmptyPage:
            page_data = data_paginator.page(data_paginator.num_pages)

        return render(request, 'searchStudent.html', {'studentsData': page_data})

    def post(self, request):
        user_search = request.POST['searchStudent']
        student_by_id = Students.objects.filter(studentID__icontains=user_search)
        student_by_name = Students.objects.filter(studentName__icontains=user_search)

        all_students = []
        for s in student_by_name:
            all_students.append(s)
        for s in student_by_id:
            all_students.append(s)

        # Lọc lại danh sách học sinh tìm được, chỉ ghi nhận các học sinh có ID khác nhau vào list students_data
        students_data = []
        if len(all_students) > 0:
            all_students.sort(key=cmp_by_student_id)

            for i in range(0, len(all_students)):
                if i == 0:
                    students_data.append(all_students[i])
                elif all_students[i].studentID != all_students[i - 1].studentID:
                    students_data.append(all_students[i])

        # Từ danh sách các học sinh khác nhau, tạo ra list tuple, mỗi tuple là tên học sinh + khóa học đang tham gia.
        last_data = []
        if len(students_data) > 0:
            for student in students_data:
                courses = student.belongToCourse.all()
                for course in courses:
                    last_data.append({'student': student, 'course': course})

        data_paginator = Paginator(last_data, 6)
        page = request.GET.get('page', 1)
        try:
            page_data = data_paginator.page(page)
        except PageNotAnInteger:
            page_data = data_paginator.page(1)
        except EmptyPage:
            page_data = data_paginator.page(data_paginator.num_pages)

        return render(request, 'searchStudent.html', {'studentsData': page_data})


def cmp_teacher_by_id(element):
    return element.teacherID


class SearchTeacher(View):
    def get(self, request):
        teacher_data = Teachers.objects.all().order_by("teacherName")

        data_paginator = Paginator(teacher_data, 6)
        page = request.GET.get('page', 1)
        try:
            page_data = data_paginator.page(page)
        except PageNotAnInteger:
            page_data = data_paginator.page(1)
        except EmptyPage:
            page_data = data_paginator.page(data_paginator.num_pages)

        return render(request, 'searchTeacher.html', {'teacherData': page_data})

    def post(self, request):
        user_search = request.POST['searchTeacher']
        teacher_by_id = Teachers.objects.filter(teacherID__icontains=user_search)
        teacher_by_name = Teachers.objects.filter(teacherName__icontains=user_search)

        teacher_list = []
        for t in teacher_by_name:
            teacher_list.append(t)
        for t in teacher_by_id:
            teacher_list.append(t)

        if len(teacher_list) > 0:
            teacher_list.sort(key=cmp_teacher_by_id)
            new_list = [teacher_list[0]]

            for i in range(1, len(teacher_list)):
                if teacher_list[i].teacherID != teacher_list[i - 1].teacherID:
                    new_list.append(teacher_list[i])

        data_paginator = Paginator(new_list, 6)
        page = request.GET.get('page', 1)
        try:
            page_data = data_paginator.page(page)
        except PageNotAnInteger:
            page_data = data_paginator.page(1)
        except EmptyPage:
            page_data = data_paginator.page(data_paginator.num_pages)

        return render(request, "searchTeacher.html", {'teacherData': page_data})


@login_required(login_url='login')
def profile_page(request):
    full_name = request.user.teachers.teacherName
    email = request.user.teachers.teacherEmail
    phone = request.user.teachers.phoneNumber
    DOB = request.user.teachers.teacherDOB

    context = {
        'fullName': full_name,
        'email': email,
        'phoneNumber': phone,
        'DOB': DOB
    }

    return render(request, 'profile.html', context)
