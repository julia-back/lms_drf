from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from .models import CustomUser, Payment
from .permissions import IsCurrentUser
from .serializers import (CustomUserPrivateSerializer, CustomUserPublicSerializer, CustomUserRegisterSerializer,
                          PaymentSerializer)


class CustomUserRegisterAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserRegisterSerializer


class CustomUserListAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserPublicSerializer


class CustomUserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        if self.request.user == self.get_object():
            return CustomUserPrivateSerializer
        return CustomUserPublicSerializer


class CustomUserUpdateAPIview(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserPrivateSerializer
    permission_classes = [IsCurrentUser]


class CustomUserDestroyApIView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsCurrentUser]


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsCurrentUser]
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ["date"]
    filterset_fields = ["course", "lesson", "payment_method"]
