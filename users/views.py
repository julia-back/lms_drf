from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, views
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from materials.models import Course

from .models import CustomUser, Payment, Subscription
from .permissions import IsCurrentUser
from .services import get_payment_link
from .serializers import (CustomUserPrivateSerializer, CustomUserPublicSerializer, CustomUserRegisterSerializer,
                          PaymentCreateSerializer, PaymentListSerializer, SubscriptionSerializer)


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
    serializer_class = CustomUserPublicSerializer
    permission_classes = [IsCurrentUser]


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentCreateSerializer

    def perform_create(self, serializer):
        user = self.request.user
        data = serializer.validated_data
        product = data.get("course") if data.get("course") else data.get("lesson")
        amount = product.price
        if data.get("payment_method") == "cash":
            payment_link = None
        else:
            payment_link = get_payment_link(user=user, product=product, amount=amount)
        serializer.save(user=user, amount=amount, payment_link=payment_link)


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentListSerializer
    permission_classes = [IsAuthenticated, IsCurrentUser]
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ["date"]
    filterset_fields = ["course", "lesson", "payment_method"]


class SubscriptionAPIView(views.APIView):

    def post(self, request, course_id):
        user = request.user
        try:
            course = Course.objects.filter(id=course_id).get()
        except ObjectDoesNotExist:
            return Response({"message": "Объект курса не найден"})
        subs = Subscription.objects.filter(user=user, course=course)
        if subs.exists():
            subs.delete()
            return Response({"message": "Объект подписки успешно удален"})
        else:
            subs = Subscription.objects.create(user=user, course=course)
            return JsonResponse(SubscriptionSerializer(subs).data)
