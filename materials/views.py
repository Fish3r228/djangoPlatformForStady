from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect
from .models import Course, Lesson, CourseSubscription
from .serializers import CourseSerializer, LessonSerializer
from .paginators import CoursePagination, LessonPagination
from .tasks import send_course_update_email
from datetime import timedelta
from django.utils.timezone import now


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CoursePagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LessonPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)


class SubscribeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        subs_item = CourseSubscription.objects.filter(user=user, course=course)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        else:
            CourseSubscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"

        return Response({"message": message})

def update_course(request, pk):
    """
    Обновление курса и асинхронная рассылка подписчикам
    """
    course = get_object_or_404(Course, pk=pk)

    # Обновляем поля курса
    course.title = request.POST.get("title", course.title)
    course.save()

    # Получаем список email подписчиков
    subscribers = course.subscribers.all().values_list("email", flat=True)

    # Отправляем письма, если есть подписчики и курс не обновлялся более 4 часов
    if subscribers and (now() - course.updated_at > timedelta(hours=4)):
        send_course_update_email.delay(course.id, list(subscribers))

    # Редирект на страницу курса
    return redirect("materials:course_detail", pk=course.pk)