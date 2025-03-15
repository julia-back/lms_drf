from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views
from .apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(permission_classes=[AllowAny]), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=[AllowAny]), name="token_refresh"),

    path("user_register/", views.CustomUserRegisterAPIView.as_view(permission_classes=[AllowAny]),
         name="user_register"),
    path("user_list/", views.CustomUserListAPIView.as_view(), name="user_list"),
    path("user_detail/<int:pk>/", views.CustomUserRetrieveAPIView.as_view(), name="user_detail"),
    path("user_update/<int:pk>/", views.CustomUserUpdateAPIview.as_view(), name="user_update"),
    path("user_delete/<int:pk>/", views.CustomUserDestroyApIView.as_view(), name="user_delete"),

    path("payment_create/", views.PaymentCreateAPIView.as_view(), name="payment_create"),
    path("payment_list/", views.PaymentListAPIView.as_view(), name="payment_list"),

    path("subscription/<int:course_id>/", views.SubscriptionAPIView.as_view(), name="subscription"),
]
