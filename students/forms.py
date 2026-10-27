from django import forms
# pyrefly: ignore [missing-import]
from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'course', 'grade', 'study_hours_per_week']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'student@example.com'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'grade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0 - 100', 'step': '0.5', 'min': '0', 'max': '100'}),
            'study_hours_per_week': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Weekly hours (e.g. 15)', 'step': '0.5', 'min': '0'}),
        }
