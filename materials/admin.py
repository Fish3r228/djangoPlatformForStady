from django.contrib import admin
from .models import Course, Lesson

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')  # убрал 'created_at'
    search_fields = ('title',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course')  # убрал 'order'
    list_filter = ('course',)
    search_fields = ('title',)
