from .models import Course, Lesson
from datetime import timedelta
from django.utils import timezone


def is_difference_updated_at_more_4_hours(course_id=None, lesson_id=None):
    """
    Проверяет, что с последнего обновления курса или его уроков
    прошло более 4 часов. Возвращает True или False.
    """
    if course_id:
        course = Course.objects.filter(id=course_id).first()
    if lesson_id:
        course = Lesson.objects.filter(id=lesson_id).first().course
    if course_id and lesson_id:
        raise ValueError("Введите либо id курса, либо id урока.")
    difference = timezone.now() - course.updated_at
    if difference > timedelta(hours=4):
        return True
    return False
