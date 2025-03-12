from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsModerator

from .models import Course, Lesson
from .pagination import CustomPagination
from .permissions import IsOwner
from .serializers import CourseSerializer, LessonSerializer
from users.tasks import send_mail_update_course
from materials.services import is_difference_updated_at_more_4_hours
from django.utils import timezone


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, updated_at=timezone.now())

    def perform_update(self, serializer):
        course_id = self.request.parser_context.get("kwargs").get("pk")
        is_enough_difference = is_difference_updated_at_more_4_hours(course_id=course_id)
        course = serializer.save(updated_at=timezone.now())
        if is_enough_difference:
            emails = [subscription.user.email for subscription in course.subscription_set.all()]
            course_name = course.name
            send_mail_update_course.delay(course_name, emails)

    def get_permissions(self):

        if self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        if self.action in ["retrieve", "update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        if self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsOwner]
        return super().get_permissions()


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    def perform_update(self, serializer):
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
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]
