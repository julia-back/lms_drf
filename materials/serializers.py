from rest_framework import serializers

from .models import Course, Lesson
from .validators import YoutubeLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [YoutubeLinkValidator(field="video_link")]


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lesson_set = LessonSerializer(many=True, read_only=True)
    subscription = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_lesson_count(self, instance):
        return instance.lesson_set.count()

    def get_subscription(self, instance):
        return instance.subscription_set.filter(user=self.context.get("request").user).exists()
