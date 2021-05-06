from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views import View


def home_page(request):
    return render(request, 'home.html')


def home_log_page(request):
    return render(request, 'home_log.html')


def search_page(request):
    return render(request, 'search.html')


class ProfilePage(View):
    def get(self, request):
        return render(request, 'profile.html')


class ManagePage(View):
    def get(self, request):
        return render(request, 'manage.html')


class AddStudentPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'addStudent.html')
        else:
            return render(request, 'login.html')


class LoginUser(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user = request.POST['userName']
        user_pass = request.POST['userPassword']
        this_user = authenticate(username=user, password=user_pass)

        if this_user is not None:
            return render(request, 'home_log.html')
        else:
            # login_unsuccessful = 1;
            login(request, this_user)
            return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return render(request, 'home_log.html')
