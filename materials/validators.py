from rest_framework import serializers

def validate_youtube_url(value):
    """
    Валидатор: разрешаем только ссылки на youtube.com
    """
    if "youtube.com" not in value and "youtu.be" not in value:
        raise serializers.ValidationError("Можно добавлять только ссылки на youtube.com")
    return value
