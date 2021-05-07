from django.db import models
from django.contrib.auth.models import User


class WebUser(models.Model):
    web_user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def get_name(self):
        return self.web_user.first_name + " " + self.web_user.last_name

    @property
    def get_instance(self):
        return self

    def __str__(self):
        return self.web_user.last_name


class CourseList(models.Model):
    courseID = models.CharField(max_length=20)
    manageTeacher = models.ForeignKey(WebUser, on_delete=models.CASCADE)
    studentNumber = models.IntegerField()
    level = models.CharField(max_length=10)
    tuitionFees = models.IntegerField()
    schedule = models.CharField(max_length=50)


class Students(models.Model):
    studentID = models.CharField(max_length=20)
    studentName = models.CharField(max_length=50)
    DOB = models.DateTimeField()
    studentGender = models.CharField(max_length=6)
    parentsPhoneNumber = models.CharField(max_length=10)
    studentEmail = models.EmailField()
    courseID = models.ForeignKey(CourseList, on_delete=models.CASCADE)