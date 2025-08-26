from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from materials.models import Course, CourseSubscription

User = get_user_model()

class SubscriptionTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="12345")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="Django", description="test", owner=self.user)

    def test_subscribe_unsubscribe(self):
        response = self.client.post("/api/materials/subscriptions/", {"course_id": self.course.id})
        self.assertEqual(response.data["message"], "Подписка добавлена")
        self.assertTrue(CourseSubscription.objects.filter(user=self.user, course=self.course).exists())

        response = self.client.post("/api/materials/subscriptions/", {"course_id": self.course.id})
        self.assertEqual(response.data["message"], "Подписка удалена")
        self.assertFalse(CourseSubscription.objects.filter(user=self.user, course=self.course).exists())
