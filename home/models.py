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

