from django.urls import path, include
from .apps import MaterialsConfig
from rest_framework.routers import DefaultRouter
from . import views


app_name = MaterialsConfig.name

router = DefaultRouter()
router.register("courses", views.CourseViewSet, basename='course')

urlpatterns = [
    path("", include(router.urls)),
    path("lessons/", views.LessonListAPIView.as_view(), name="lesson_list"),
    path("lessons/<int:pk>/", views.LessonRetrieveAPIView.as_view(), name="lesson_detail"),
    path("lessons/", views.LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lessons/<int:pk>/", views.LessonUpdateAPIView.as_view(), name="lesson_update"),
    path("lessons/<int:pk>/", views.LessonDestroyAPIView.as_view(), name="lesson_delete"),
]
