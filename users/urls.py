from django.urls import path
from .apps import UsersConfig
from . import views


app_name = UsersConfig.name

urlpatterns = [
    path("user_detail/<int:pk>/", views.CustomUserRetrieveAPIView.as_view(), name="user_detail"),
    path("user_update/<int:pk>/", views.CustomUserUpdateAPIview.as_view(), name="user_update"),
]
