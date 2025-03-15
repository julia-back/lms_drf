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
from .serializers import (CustomUserPrivateSerializer, CustomUserPublicSerializer, CustomUserRegisterSerializer,
                          PaymentCreateSerializer, PaymentListSerializer, SubscriptionSerializer)
from .services import PaymentLink


class CustomUserRegisterAPIView(generics.CreateAPIView):
    """Представление для регистрации / создания модели пользователя."""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserRegisterSerializer


class CustomUserListAPIView(generics.ListAPIView):
    """Представление для получения списка объектов моледи пользователя."""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserPublicSerializer


class CustomUserRetrieveAPIView(generics.RetrieveAPIView):
    """
    Представление для просмотра объекта модели пользователя. Использует
    сериализатор в зависимости от того, запрашивает ли текущий авторизованный
    пользователь свою модель пользователя.
    """

    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        """
        Переопределенный метод получения сериализатора. Возвращает сериализатор
        в зависимости от того, запрашивает ли текущий авторизованный пользователь
        свою модель пользователя.
        """

        if self.request.user == self.get_object():
            return CustomUserPrivateSerializer
        return CustomUserPublicSerializer


class CustomUserUpdateAPIview(generics.UpdateAPIView):
    """
    Представление для обновления модели пользователя. Доступно текущему
    авторизованному пользователю, запрашивающему свою модель пользователя.
    """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserPrivateSerializer
    permission_classes = [IsCurrentUser]


class CustomUserDestroyApIView(generics.DestroyAPIView):
    """
    Представление для удаления модели пользователя. Доступно текущему
    авторизованному пользователю, запрашивающему свою модель пользователя.
    """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserPublicSerializer
    permission_classes = [IsCurrentUser]


class PaymentCreateAPIView(generics.CreateAPIView):
    """Представление для создания объекта модели платежа. """

    serializer_class = PaymentCreateSerializer

    def perform_create(self, serializer):
        """
        Переопределнный метод создания объекта модели платежа.
        В ответе содержит ссылку на оплату.
        """

        user = self.request.user
        data = serializer.validated_data
        product = data.get("course") if data.get("course") else data.get("lesson")
        amount = product.price
        if data.get("payment_method") == "cash":
            payment_link = None
        else:
            payment_link = PaymentLink(user_obj=user, product_obj=product).get_payment_link()
        serializer.save(user=user, amount=amount, payment_link=payment_link)


class PaymentListAPIView(generics.ListAPIView):
    """Представление для получения списка объектов модели платежа."""

    queryset = Payment.objects.all()
    serializer_class = PaymentListSerializer
    permission_classes = [IsAuthenticated, IsCurrentUser]
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ["date"]
    filterset_fields = ["course", "lesson", "payment_method"]


class SubscriptionAPIView(views.APIView):
    """Представление для создания и удаления объекта модели подписки."""

    def post(self, request, course_id):
        """Метод создания подписки, если ее нет, и удаления подписки, если она есть."""

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
