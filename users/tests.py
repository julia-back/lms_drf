from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course

from .models import CustomUser, Subscription


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(email="test@test.com")
        self.course = Course.objects.create(name="test course",
                                            img=None,
                                            description="test course",
                                            owner=None)
        self.url = reverse("users:subscription", args=[self.course.id])

    def test_subscription_no_authenticated(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subscription_on(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("user"), self.user.id)
        self.assertEqual(data.get("course"), self.course.id)

    def test_subscription_off(self):
        Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("message"), "Объект подписки успешно удален")
