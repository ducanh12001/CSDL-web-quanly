from django.db import models
from django.contrib.auth.models import User


class Teachers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    teacherID = models.CharField(max_length=10, primary_key=True, default=None)
    teacherName = models.CharField(max_length=200, null=True)
    teacherGender = models.CharField(max_length=6, null=True)
    phoneNumber = models.CharField(max_length=200, null=True)
    teacherEmail = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.teacherName


class CourseList(models.Model):
    courseID = models.CharField(max_length=20, primary_key=True)
    courseName = models.CharField(max_length=100, null=True, default=None)
    manageTeacher = models.ForeignKey(Teachers, null=True, on_delete=models.SET_NULL)
    studentNumber = models.IntegerField(default=0)
    level = models.CharField(max_length=10)
    tuitionFeesByVND = models.IntegerField()
    schedule = models.CharField(max_length=50)
    courseLengthByMonth = models.IntegerField(default=0)
    beginDate = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=200, null=True, blank=True, default=None)
    studyRoom = models.CharField(max_length=200, null=True)


class Students(models.Model):
    studentID = models.CharField(max_length=20, primary_key=True)
    studentName = models.CharField(max_length=50)
    studentEmail = models.CharField(max_length=100, null=True)
    DOB = models.DateTimeField(default=None)
    studentGender = models.CharField(max_length=6, null=True, default=None)
    phoneNumber = models.CharField(max_length=10, null=True, default=None)
    studentEmail = models.EmailField(default=None)
    belongToCourse = models.ManyToManyField(CourseList)


class StudentResult(models.Model):
    belongToStudent = models.ForeignKey(Students, null=True, on_delete=models.SET_NULL)
    absentDays = models.IntegerField(default=0)
    GPA = models.FloatField(default=0.0)
