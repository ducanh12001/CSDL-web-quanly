from django.contrib import admin
from django.urls import path, include
from . import views
app_name = 'home'

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('home_log/', views.home_log_page, name='home_log'),
    path('search/', views.search_page, name='search'),
    path('profile/', views.ProfilePage.as_view(), name='profile'),
    path('management/', views.ManagePage.as_view(), name='management'),
    path('addStudent/', views.AddStudentPage.as_view(), name='add_student'),
]
