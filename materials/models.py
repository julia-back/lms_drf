from django.db import models

from config.settings import AUTH_USER_MODEL
from django.utils import timezone


class Course(models.Model):
    """Модель курса. Связана с моделью пользователя через внешний ключ."""

    name = models.CharField(max_length=250)
    img = models.ImageField(upload_to="img_course/", blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    """Модель урока. Связана с моделью курса и моделью пользователя через внешний ключ."""

    name = models.CharField(max_length=250)
    img = models.ImageField(upload_to="img_lesson/", blank=True, null=True)
    description = models.TextField()
    video_link = models.URLField(blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
