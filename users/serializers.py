from rest_framework import serializers

from .models import CustomUser, Payment, Subscription


class PaymentCreateSerializer(serializers.ModelSerializer):
    """
    Класс сериализатора для создания модели платежа. Устанавливает поле метода плтежа как
    обязательное. Проверяет, что передается одно из полей: поле, ссылающееся
    на модель курса или поле, ссылающееся на модель урока.
    """

    class Meta:
        model = Payment
        fields = ["course", "lesson", "payment_method", "payment_link"]
        extra_kwargs = {"payment_method": {"required": True}}

    def validate(self, attrs):
        """Переопределенный метод валидации. Проверяет, что передается одно из полей: course или lesson."""

        if attrs.get("course") is None and attrs.get("lesson") is None:
            raise serializers.ValidationError("Укажите курс или урок для оплаты")
        if attrs.get("course") and attrs.get("lesson"):
            raise serializers.ValidationError("Укажите только один товар для оплаты.")
        return attrs


class PaymentListSerializer(serializers.ModelSerializer):
    """Класс сериализатора для отображения списка объектов модели платежа."""

    class Meta:
        model = Payment
        fields = "__all__"


class CustomUserPrivateSerializer(serializers.ModelSerializer):
    """
    Класс сериализатора модели пользователя. Используется для предоставления
    возможности просмотра, обновления и удаления текущему авторизованному пользователю своей модели пользователя.
    """

    payment_set = PaymentListSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "country", "email", "phone_number", "avatar", "payment_set"]


class CustomUserPublicSerializer(serializers.ModelSerializer):
    """
    Класс сериализатора модели пользователя. Используется для предоставления
    возможности просмотра объекта модели другим пользователям.
    """

    class Meta:
        model = CustomUser
        fields = ["username", "country", "email", "phone_number", "avatar"]


class CustomUserRegisterSerializer(serializers.ModelSerializer):
    """Класс сериализатора модели пользователя для регистрации пользователя."""

    class Meta:
        model = CustomUser
        fields = ["email", "username", "password"]

    def create(self, validated_data):
        """
        Переопределенный метод создания объекта модели пользователя.
        При сохранении хеширует введенный отвалидированный пароль.
        """

        model = self.Meta.model
        instance = model.objects.create(**validated_data)
        instance.set_password(instance.password)
        instance.save()
        return instance


class SubscriptionSerializer(serializers.ModelSerializer):
    """Класс сериализатора модели подписки."""

    class Meta:
        model = Subscription
        fields = "__all__"
