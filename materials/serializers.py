from rest_framework import serializers

from .models import Course, Lesson
from .validators import YoutubeLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    """Класс сериализатора модели урока."""

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [YoutubeLinkValidator(field="video_link")]


class CourseSerializer(serializers.ModelSerializer):
    """
    Класс сериализатора модели курса. С дополинельными полями:
    lesson_count - количество связанных к курсом уроков,
    lesson_set - список связанных с курсом уроков,
    subscription - признак наличия у пользователя подписки на обновления курса.
    """

    lesson_count = serializers.SerializerMethodField()
    lesson_set = LessonSerializer(many=True, read_only=True)
    subscription = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_lesson_count(self, instance):
        """Метод получения поля количества связанных уроков"""

        return instance.lesson_set.count()

    def get_subscription(self, instance):
        """
        Метод получения признака наличия подписки на обновления курса у
        текущего авторизованного пользователя
        """
        return instance.subscription_set.filter(user=self.context.get("request").user).exists()
