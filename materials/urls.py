from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CourseViewSet, LessonViewSet, SubscribeAPIView

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')

urlpatterns = [
    path('', include(router.urls)),
    path('subscribe/', SubscribeAPIView.as_view(), name='subscribe'),
]
