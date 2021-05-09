from django.contrib import admin
from .models import Teachers, CourseList, Students, StudentResult


admin.site.register(Teachers)
admin.site.register(CourseList)
admin.site.register(Students)
admin.site.register(StudentResult)