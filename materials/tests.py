from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import CustomUser

from .models import Lesson


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(email="test@test.com")
        self.lesson_1 = Lesson.objects.create(name="lesson_1", description="description_1",
                                              owner=self.user)
        self.lesson_2 = Lesson.objects.create(name="lesson_2", description="description_2")

    def test_lesson_list_no_authenticated(self):
        url = reverse("materials:lesson_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_list_ok(self):
        url = reverse("materials:lesson_list")
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        data = response.json()
        expected_result = {'count': 2, 'next': None, 'previous': None,
                           'results': [
                               {'id': self.lesson_1.id,
                                'name': self.lesson_1.name,
                                'img': self.lesson_1.img,
                                'description': self.lesson_1.description,
                                'video_link': self.lesson_1.video_link,
                                'course': self.lesson_1.course,
                                'owner': self.lesson_1.owner.pk},
                               {'id': self.lesson_2.id,
                                'name': self.lesson_2.name,
                                'img': self.lesson_2.img,
                                'description': self.lesson_2.description,
                                'video_link': self.lesson_2.video_link,
                                'course': self.lesson_2.course,
                                'owner': self.lesson_2.owner}]}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, expected_result)

    def test_lesson_detail_no_authenticated(self):
        url = reverse("materials:lesson_detail", args=[self.lesson_2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_detail_not_permission(self):
        url = reverse("materials:lesson_detail", args=[self.lesson_2.id])
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_detail_ok(self):
        url = reverse("materials:lesson_detail", args=[self.lesson_1.id])
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_create_no_authenticated(self):
        url = reverse("materials:lesson_create")
        data_to_create = {"name": "test create", "description": "test create"}
        response = self.client.post(url, data_to_create)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_create_ok(self):
        url = reverse("materials:lesson_create")
        data_to_create = {"name": "test create", "description": "test create"}
        self.client.force_authenticate(self.user)
        response = self.client.post(url, data_to_create)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lesson_update_put_no_authenticated(self):
        url = reverse("materials:lesson_update", args=[self.lesson_2.id])
        data_to_update = {"name": "test update",
                          "description": "test update"}
        response = self.client.put(url, data_to_update)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_update_put_not_permission(self):
        url = reverse("materials:lesson_update", args=[self.lesson_2.id])
        data_to_update = {"name": "test update",
                          "description": "test update"}
        self.client.force_authenticate(self.user)
        response = self.client.put(url, data_to_update)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_update_put_ok(self):
        url = reverse("materials:lesson_update", args=[self.lesson_1.id])
        data_to_update = {"name": "test update",
                          "description": "test update"}
        self.client.force_authenticate(self.user)
        response = self.client.put(url, data_to_update)
        data = response.json()
        expected_result = {'id': self.lesson_1.id,
                           'name': data_to_update.get("name"),
                           'img': self.lesson_1.img,
                           'description': data_to_update.get("description"),
                           'video_link': self.lesson_1.video_link,
                           'course': self.lesson_1.course,
                           'owner': self.lesson_1.owner.pk}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, expected_result)

    def test_lesson_update_patch_no_authenticated(self):
        url = reverse("materials:lesson_update", args=[self.lesson_2.id])
        data_to_update = {"name": "test update"}
        response = self.client.patch(url, data_to_update)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_update_patch_not_permission(self):
        url = reverse("materials:lesson_update", args=[self.lesson_2.id])
        data_to_update = {"name": "test update"}
        self.client.force_authenticate(self.user)
        response = self.client.patch(url, data_to_update)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_update_patch_ok(self):
        url = reverse("materials:lesson_update", args=[self.lesson_1.id])
        data_to_update = {"name": "test update"}
        self.client.force_authenticate(self.user)
        response = self.client.patch(url, data_to_update)
        data = response.json()
        expected_result = {'id': self.lesson_1.id,
                           'name': data_to_update.get("name"),
                           'img': self.lesson_1.img,
                           'description': self.lesson_1.description,
                           'video_link': self.lesson_1.video_link,
                           'course': self.lesson_1.course,
                           'owner': self.lesson_1.owner.pk}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, expected_result)

    def test_lesson_delete_no_authenticated(self):
        url = reverse("materials:lesson_delete", args=[self.lesson_2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_delete_not_permission(self):
        url = reverse("materials:lesson_delete", args=[self.lesson_2.id])
        self.client.force_authenticate(self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_delete_ok(self):
        url = reverse("materials:lesson_delete", args=[self.lesson_1.id])
        self.client.force_authenticate(self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
