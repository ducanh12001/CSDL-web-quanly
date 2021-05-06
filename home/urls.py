from django.contrib import admin
from django.urls import path, include
from . import views
app_name = 'home'

urlpatterns = [
    path('', views.LoginUser.as_view(), name='login'),
    path('home/', views.home_page, name='home_page'),
    path('home_log/', views.home_log_page, name='home_log'),
    path('search/', views.search_page, name='search'),
    path('profile/', views.ProfilePage.as_view(), name='profile'),
    path('manage/', views.ManagePage.as_view(), name='manage'),
    path('addStudent/', views.AddStudentPage.as_view(), name='add_student'),
]
