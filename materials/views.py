from django.utils import timezone
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from materials.services import is_difference_updated_at_more_4_hours
from users.permissions import IsModerator
from users.tasks import send_mail_update_course

from .models import Course, Lesson
from .pagination import CustomPagination
from .permissions import IsOwner
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для модели курса."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        """
        Переопределенный метод создания объекта курса.
        При сохранении объекта устанавливает в поле владельца
        текущего авторизованного пользователя.
        """

        serializer.save(owner=self.request.user, updated_at=timezone.now())

    def perform_update(self, serializer):
        """
        Переопределенный метод обновления объекта.
        При обновлении объекта курса отправляется сообщение пользователям, подписанным на
        обновления курса, при условии, что с момента последнего обновления прошло более 4 часов.
        Также обновляет поле updated_at объекта курса.
        """

        course_id = self.request.parser_context.get("kwargs").get("pk")
        is_enough_difference = is_difference_updated_at_more_4_hours(course_id=course_id)
        course = serializer.save(updated_at=timezone.now())
        if is_enough_difference:
            emails = [subscription.user.email for subscription in course.subscription_set.all()]
            course_name = course.name
            send_mail_update_course.delay(course_name, emails)

    def get_permissions(self):
        """Переопределенный метод полученяи разрешений. Устанавливает разрешения
         ля пользователей в зависимости от метода запроса."""

        if self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        if self.action in ["retrieve", "update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        if self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsOwner]
        return super().get_permissions()


class LessonListAPIView(generics.ListAPIView):
    """
    Представление для получения списка объектов модели урока.
    Доступен только авторизованным пользователям (разрешение доступа только
    авторизованным пользователям установлено на уровне проекта в settings.py)
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Представление для получения конкретного объекта модели урока.
    Доступно только владельца урока и пользователя, находящегося в группе модераторов.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonCreateAPIView(generics.CreateAPIView):
    """
    Представление для создания объекта модели урока.
    Доступно всем авторизованным пользователям, кроме пользователей, состоящих в группе модераторов.
    """

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        """
        Переопределнный метод создания объекта модели урока. При сохранении объекта
        устанавливает в поле владельца текущего авторизованного пользователя.
        """

        serializer.save(owner=self.request.user)


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Представление для обновления объекта модели урока. Доступно владельцу
    объекта урока и пользователям, состоящих в группе модераторов.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    def perform_update(self, serializer):
        """
        Переопределенный метод обновления объекта модели урока. Отправляет
        сообщение пользователям, подписанным на обновления курса, с которым связан урок,
        при условии, что с момента последнего обновления прошло более 4 часов.
        Обновляет поле updated_at объекта курса, с которым связан текущий объект урока.
        """

        lesson_id = self.request.parser_context.get("kwargs").get("pk")
        is_enough_difference = is_difference_updated_at_more_4_hours(lesson_id=lesson_id)
        lesson = serializer.save()
        course = lesson.course
        course.updated_at = timezone.now()
        course.save()
        if is_enough_difference:
            emails = [subscription.user.email for subscription in course.subscription_set.all()]
            course_name = course.name
            send_mail_update_course.delay(course_name, emails)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Представление для удаления объекта модели урока. Доступно владельцу объекта урока и
    пользователям, состоящим в группе модераторов.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]
