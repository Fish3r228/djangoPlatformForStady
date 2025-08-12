# users/serializers.py
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from materials.serializers import CourseSerializer, LessonSerializer
from .models import Payment

User = get_user_model()


# ===== Регистрация пользователя =====
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',        # убрал 'username'
            'password',
            'password2',
            'first_name',
            'last_name',
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user



# ===== Сериализатор платежей =====
class PaymentSerializer(serializers.ModelSerializer):
    paid_course = CourseSerializer(read_only=True)
    paid_lesson = LessonSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id',
            'user',
            'paid_course',
            'paid_lesson',
            'amount',
            'payment_date',
            'payment_method'
        ]


# ===== Сериализатор пользователя =====
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']  # без username
