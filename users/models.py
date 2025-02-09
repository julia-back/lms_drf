from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=250)
    avatar = models.ImageField(upload_to="avatar/")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
