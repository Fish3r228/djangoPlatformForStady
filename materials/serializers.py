from rest_framework import serializers
from .models import Course, Lesson
from .validators import validate_youtube_url


class CourseSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.email")
    is_subscribed = serializers.SerializerMethodField()  # признак подписки

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'owner', 'is_subscribed']
        read_only_fields = ['owner']

    def get_is_subscribed(self, obj):
        """Проверяем подписку текущего пользователя на курс"""
        user = self.context['request'].user
        return obj.subscriptions.filter(user=user).exists()


class LessonSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.email")
    video_url = serializers.CharField(validators=[validate_youtube_url], required=False)

    class Meta:
        model = Lesson
        fields = ['id', 'course', 'title', 'content', 'video_url', 'owner']
        read_only_fields = ['owner']
