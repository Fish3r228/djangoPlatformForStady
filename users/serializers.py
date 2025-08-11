from rest_framework import serializers
from .models import User, Payment
from materials.serializers import CourseSerializer, LessonSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'city', 'avatar', 'is_staff')
        read_only_fields = ('is_staff',)


class PaymentSerializer(serializers.ModelSerializer):
    paid_course = CourseSerializer(read_only=True)
    paid_lesson = LessonSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'user', 'paid_course', 'paid_lesson', 'amount', 'payment_date', 'payment_method']