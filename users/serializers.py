from rest_framework import serializers

from .models import CustomUser, Payment, Subscription


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["course", "lesson", "payment_method", "payment_link"]
        extra_kwargs = {"payment_method": {"required": True}}

    def validate(self, attrs):
        if attrs.get("course") is None and attrs.get("lesson") is None:
            raise serializers.ValidationError("Укажите курс или урок для оплаты")
        if attrs.get("course") and attrs.get("lesson"):
            raise serializers.ValidationError("Укажите только один товар для оплаты.")
        return attrs


class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class CustomUserPrivateSerializer(serializers.ModelSerializer):

    payment_set = PaymentListSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "country", "email", "phone_number", "avatar", "payment_set"]


class CustomUserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "country", "email", "phone_number", "avatar"]


class CustomUserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "username", "password"]

    def create(self, validated_data):
        model = self.Meta.model
        instance = model.objects.create(**validated_data)
        instance.set_password(instance.password)
        instance.save()
        return instance


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
