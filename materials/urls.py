from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from .apps import MaterialsConfig

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register("course", views.CourseViewSet, basename='course')

urlpatterns = [
    path("", include(router.urls)),
    path("lesson_list/", views.LessonListAPIView.as_view(), name="lesson_list"),
    path("lesson_detail/<int:pk>/", views.LessonRetrieveAPIView.as_view(), name="lesson_detail"),
    path("lesson_create/", views.LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lesson_update/<int:pk>/", views.LessonUpdateAPIView.as_view(), name="lesson_update"),
    path("lesson_delete/<int:pk>/", views.LessonDestroyAPIView.as_view(), name="lesson_delete"),
]
