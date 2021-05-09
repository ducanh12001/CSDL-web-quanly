from django.contrib import admin
from django.urls import path, include
from . import views
app_name = 'home'

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('home_log/', views.home_log_page, name='home_log'),
    path('search/search_class', views.SearchClass.as_view(), name='searchClass'),
    path('search/search_student', views.SearchStudent.as_view(), name='searchStudent'),
    path('search/search_teacher', views.SearchTeacher.as_view(), name='searchTeacher'),
    path('management/', views.ManagePage.as_view(), name='management'),
    path('addStudent/', views.AddStudentPage.as_view(), name='add_student'),
    path('logout', views.logout_user, name='logout'),
]
