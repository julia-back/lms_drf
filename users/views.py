from rest_framework import generics
from .models import CustomUser
from .serializers import CustomUserSerializer


class CustomUserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CustomUserUpdateAPIview(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
