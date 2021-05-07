from django.db import models
from django.contrib.auth.models import User


class WebUser(models.Model):
    web_user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacherID = models.CharField(max_length=10, primary_key=True)

    @property
    def get_name(self):
        return self.web_user.first_name + " " + self.web_user.last_name

    @property
    def get_instance(self):
        return self

    def __str__(self):
        return self.web_user.last_name


class CourseList(models.Model):
    courseID = models.CharField(max_length=20, blank=False, primary_key=True)
    teacherID = models.ForeignKey(WebUser, on_delete=models.CASCADE)
    studentNumber = models.IntegerField(default=0)
    level = models.CharField(max_length=10)
    tuitionFees = models.IntegerField()
    schedule = models.CharField(max_length=50)
    timeLastByMonth = models.IntegerField(default=0)
    beginDate = models.DateTimeField(auto_now_add=True)


class Students(models.Model):
    studentID = models.CharField(max_length=20, primary_key=True)
    studentName = models.CharField(max_length=50)
    DOB = models.DateTimeField(default=None)
    studentGender = models.CharField(max_length=6, blank=False, default=None)
    parentsPhoneNumber = models.CharField(max_length=10, default=None)
    studentEmail = models.EmailField(default=None)
    courseID = models.ManyToManyField(CourseList)


class StudentResult(models.Model):
    studentID = models.ForeignKey(Students, null=True, blank=False, on_delete=models.CASCADE)
    absentDays = models.IntegerField(default=0)
    GPA = models.FloatField(default=0.0)
