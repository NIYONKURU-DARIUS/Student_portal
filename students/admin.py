from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'course', 'grade', 'study_hours_per_week', 'registration_date')
    list_filter = ('course', 'registration_date')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('-id'