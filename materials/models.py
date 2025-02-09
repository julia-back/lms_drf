from django.db import models


class Course(models.Model):

    name = models.CharField(max_length=250)
    img = models.ImageField(upload_to="img_course/")
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):

    name = models.CharField(max_length=250)
    img = models.ImageField(upload_to="img_lesson/")
    description = models.TextField()
    video_link = models.URLField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
