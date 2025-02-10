from django.urls import path
from .apps import UsersConfig
from . import views


app_name = UsersConfig.name

urlpatterns = [
    path("users/<int:pk>/", views.CustomUserRetrieveAPIView.as_view(), name="user_detail"),
    path("users/<int:pk>/", views.CustomUserUpdateAPIview.as_view(), name="user_update"),
]
