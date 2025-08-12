from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .permissions import IsModerator, IsOwner
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('-created_at')
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]  # просмотр доступен всем авторизованным
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsModerator | IsOwner]  # редактируют модераторы или владельцы
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]  # создавать могут все авторизованные (можно расширить логику)
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsOwner]  # удалять могут только владельцы
        else:
            permission_classes = [IsAuthenticated]

        return [perm() for perm in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all().order_by('order', 'created_at')
    serializer_class = LessonSerializer

    permission_classes = [IsAuthenticated]  # доступ только авторизованным

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # привязка владельца


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method in ('GET',):
            permission_classes = [IsAuthenticated]  # просмотр для авторизованных
        elif self.request.method in ('PUT', 'PATCH'):
            permission_classes = [IsAuthenticated, IsModerator | IsOwner]  # редактируют модераторы и владельцы
        elif self.request.method == 'DELETE':
            permission_classes = [IsAuthenticated, IsOwner]  # удалять могут только владельцы
        else:
            permission_classes = [IsAuthenticated]

        return [perm() for perm in permission_classes]
