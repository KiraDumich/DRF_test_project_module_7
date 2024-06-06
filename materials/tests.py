
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@example.com")
        self.course = Course.objects.create(name="Test", description="...")
        self.lesson = Lesson.objects.create(lesson_name="Урок 1", lesson_description="Введение", course=self.course,
                                            owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("materials:lesson_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("lesson_name"), self.lesson.lesson_name
        )

    def test_lesson_create(self):
        url = reverse("materials:lesson-create")
        data = {
            "lesson_name": "Урок_2"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.filter(lesson_name="Урок_2").count(), 1
        )

    def test_lesson_update(self):
        url = reverse("materials:lesson-update", args=(self.lesson.pk,))
        data = {
            "lesson_name": "Урок_2"
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("lesson_name"), "Урок_2"
        )

    def test_lesson_delete(self):
        url = reverse("materials:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        url = reverse("materials:lesson_list")
        response = self.client.get(url)
        data = response.json()
        print(data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        result = {
                  "count": 1,
                  "next": None,
                  "previous": None,
                  "results": [
                             {
                              "id": self.lesson.pk,
                              "lesson_name": self.lesson.lesson_name,
                              "lesson_description": self.lesson.lesson_description,
                              "preview": None,
                              "lesson_url": None,
                              "course": self.course.pk,
                              "owner": self.user.pk
                              }
                              ]
                }
        self.assertEqual(
            data, result
        )


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@example.com")
        self.course = Course.objects.create(name="Test", description="...", owner=self.user)
        self.lesson = Lesson.objects.create(lesson_name="Урок 1", lesson_description="Введение", course=self.course,
                                            owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), self.course.name
        )

    def test_course_create(self):
        url = reverse("materials:course-list")
        data = {"name": "Математический анализ"}
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Course.objects.all().count(), 2
        )

    def test_course_update(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        data = {
            "name": "Линейная алгебра"
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), "Линейная алгебра"
        )

    def test_course_delete(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Course.objects.all().count(), 0
        )

    def test_course_list(self):
        url = reverse("materials:course-list")
        response = self.client.get(url)
        data = response.json()
        print(data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "course_lessons": [
                        {
                            "id": self.lesson.pk,
                            "lesson_name": self.lesson.lesson_name,
                            "lesson_description": self.lesson.lesson_description,
                            "preview": None,
                            "url": None,
                            "course": self.course.pk,
                            "owner": self.user.pk
                        }

                    ],
                    "lesson_count": 1,
                    "subscription": False,
                    "name": self.course.name,
                    "description": self.course.description,
                    "preview": None,
                    "owner": self.user.pk
                }
            ]
        }
        self.assertEqual(
            data, result
        )
