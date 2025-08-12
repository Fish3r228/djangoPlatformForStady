from rest_framework import serializers
from .models import Course, Lesson

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'owner']
        read_only_fields = ['owner']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'course', 'title', 'content', 'owner']
        read_only_fields = ['owner']
