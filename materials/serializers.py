from .models import Course, Lesson
from rest_framework import serializers


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_lesson_count(self, instance):
        return instance.lesson_set.count()


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
