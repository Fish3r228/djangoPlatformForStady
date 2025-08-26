from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from materials.models import Course, Lesson

User = get_user_model()

class LessonCRUDTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="12345")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="Django", description="test", owner=self.user)

    def test_create_lesson(self):
        response = self.client.post("/api/materials/lessons/", {
            "course": self.course.id,
            "title": "Lesson 1",
            "content": "Content",
            "video_link": "https://youtube.com/testvideo"
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Lesson.objects.count(), 1)
