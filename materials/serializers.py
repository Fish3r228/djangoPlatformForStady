from rest_framework import serializers
from .models import Course, Lesson

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'course', 'title', 'description', 'preview', 'video_url', 'order', 'created_at')

class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'preview', 'description', 'created_at', 'updated_at', 'lessons')
