from .models import CustomUser, Payment
from rest_framework import serializers


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class CustomUserSerializer(serializers.ModelSerializer):

    payment_set = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "country", "phone_number", "avatar", "payment_set"]
