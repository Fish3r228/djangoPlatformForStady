from rest_framework import viewsets, generics
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer

# Course: ViewSet (ModelViewSet даёт полный CRUD)
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('-created_at')
    serializer_class = CourseSerializer

# Lesson: generic views (List, Create и отдельный Retrieve/Update/Delete)
class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all().order_by('order', 'created_at')
    serializer_class = LessonSerializer

class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
