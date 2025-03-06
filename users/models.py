from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class CustomUser(AbstractUser):

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=250, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatar/", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


class Payment(models.Model):

    PAYMENT_METHOD = [("cash", "Наличные"),
                      ("remittance", "Перевод на счет")]

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    payment_method = models.CharField(choices=PAYMENT_METHOD)
    payment_link = models.URLField(max_length=1000, default=None, blank=True, null=True)

    def __str__(self):
        return f"{self.amount} - {self.course if self.course else self.lesson}, {self.user}"

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежи"


class Subscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.course}"

    class Meta:
        verbose_name = "подписка"
        verbose_name_plural = "подписки"
