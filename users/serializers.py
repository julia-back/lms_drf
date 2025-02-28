from rest_framework import serializers

from .models import CustomUser, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class CustomUserPrivateSerializer(serializers.ModelSerializer):

    payment_set = PaymentSerializer(many=True, read_only=True)

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
